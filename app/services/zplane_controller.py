from PyQt5.QtGui import QPixmap
from pyqtgraph import PlotWidget, mkPen, TextItem
from scipy import signal
from scipy.signal import freqz, butter, cheby1, cheby2, ellip, sosfreqz,lfilter ,tf2sos
from PyQt5.QtWidgets import QFileDialog, QGraphicsRectItem, QGraphicsEllipseItem, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import numpy as np
import csv
import os
import pyqtgraph as pg
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import schemdraw
import schemdraw.elements as elm

class ZPlaneController:
    def __init__(self, plot_widget ,mag_plot_widget, phase_plot_widget ,realization_plot, add_conjugate_checkbox, zeros_radio_button, poles_radio_button):
        self.plot_widget = plot_widget
        self.add_conjugate_checkbox = add_conjugate_checkbox
        self.zeros_radio_button = zeros_radio_button
        self.poles_radio_button = poles_radio_button
        self.mag_plot_widget = mag_plot_widget
        self.phase_plot_widget = phase_plot_widget
        self.realization_plot = realization_plot

        # Data storage
        self.zeros = []
        self.poles = []
        self.history = []
        self.redo_stack = []

        # Plot configuration
        self.unit_circle = self.plot_widget.plot(pen=mkPen("blue", width=3))
        self.scatter_zeros = self.plot_widget.plot(pen=None, symbol='o', symbolBrush='green', symbolSize=12)
        self.scatter_poles = self.plot_widget.plot(pen=None, symbol='x', symbolBrush='red', symbolSize=12)

        # Draw axes on the unit circle
        self.ax_h = self.plot_widget.plot([-1, 1], [0, 0], pen=mkPen('blue', width=2))
        self.ax_v = self.plot_widget.plot([0, 0], [-1, 1], pen=mkPen('blue', width=2))

        self.update_unit_circle()
        # Frequency response plots
        self.mag_response = self.mag_plot_widget.plot(pen=mkPen("green"))
        self.phase_response = self.phase_plot_widget.plot(pen=mkPen("red"))

        # Signal connections
        self.plot_widget.scene().sigMouseClicked.connect(self.on_mouse_click)

        # Filter library
        self.filter_library = {
            # None Option
            "None": lambda: (np.array([1.0]), np.array([1.0])),  # No filtering applied

            # Butterworth Filters
            "Butterworth LPF": lambda: butter(4, 0.4, btype="low", output="ba"),
            "Butterworth HPF": lambda: butter(4, 0.4, btype="high", output="ba"),
            "Butterworth BPF": lambda: butter(4, [0.3, 0.6], btype="band", output="ba"),

            # Chebyshev I Filters
            "Chebyshev I LPF": lambda: cheby1(4, 1, 0.4, btype="low", output="ba"),
            "Chebyshev I HPF": lambda: cheby1(4, 1, 0.4, btype="high", output="ba"),
            "Chebyshev I BPF": lambda: cheby1(4, 1, [0.3, 0.6], btype="band", output="ba"),

            # Chebyshev II Filters
            "Chebyshev II LPF": lambda: cheby2(4, 20, 0.4, btype="low", output="ba"),
            "Chebyshev II HPF": lambda: cheby2(4, 20, 0.4, btype="high", output="ba"),
            "Chebyshev II BPF": lambda: cheby2(4, 20, [0.3, 0.6], btype="band", output="ba"),

            # Elliptic Filters
            "Elliptic LPF": lambda: ellip(4, 1, 20, 0.4, btype="low", output="ba"),
            "Elliptic HPF": lambda: ellip(4, 1, 20, 0.4, btype="high", output="ba"),
        }

        # Initial filter selection set to None
        self.filter_selection = "None"  # Default to no filtering

    def update_z_plane_from_filter(self):
        """Update Z-plane with zeros and poles of the selected filter."""
        if self.filter_selection == "None":
            self.zeros.clear()
            self.poles.clear()
        else:
            # Get numerator (b) and denominator (a) coefficients
            b, a = self.filter_library[self.filter_selection]()
            # Compute zeros and poles
            self.zeros = list(np.roots(b))  # Zeros of the filter
            self.poles = list(np.roots(a))  # Poles of the filter

        self.save_state()
        self.update_plot()

    def update_unit_circle(self):
        """Draw the unit circle."""
        theta = np.linspace(0, 2 * np.pi, 500)
        self.unit_circle.setData(np.cos(theta), np.sin(theta))

    def update_frequency_response(self):
        """Update the magnitude and phase response plots."""
        if not (self.zeros or self.poles):
            self.mag_response.setData([], [])
            self.phase_response.setData([], [])
            return

        # Convert zeros and poles to a transfer function
        b = np.poly(self.zeros)  # Numerator coefficients
        a = np.poly(self.poles)  # Denominator coefficients
        w, h = freqz(b, a, worN=500)  # Frequency response

        # Update magnitude and phase response
        self.mag_response.setData(w / (np.pi / 2), np.abs(h))  # Scale x-axis
        self.phase_response.setData(w / (np.pi / 2), np.angle(h))

    def configure_x_axis(self, plot_widget):
        """Configure the x-axis to display ticks in multiples of π/2."""
        axis = plot_widget.getAxis('bottom')  # Get the bottom axis
        tick_values = [(i, f"{i}π/2") for i in range(0, 11)]  # Up to 5π
        ticks = [tick_values]
        axis.setTicks(ticks)

    def update_plot(self):
        """Update the Z-plane plot with zeros and poles."""
        self.scatter_zeros.setData([z.real for z in self.zeros], [z.imag for z in self.zeros])
        self.scatter_poles.setData([p.real for p in self.poles], [p.imag for p in self.poles])
        self.update_frequency_response()

    def on_mouse_click(self, event):
        """Handle mouse click to add zeros/poles."""
        if not self.plot_widget.sceneBoundingRect().contains(event.scenePos()):
            return

        mouse_point = self.plot_widget.getViewBox().mapSceneToView(event.scenePos())
        x, y = mouse_point.x(), mouse_point.y()
        if np.sqrt(x ** 2 + y ** 2) > 1.2:  # Limit placement outside the unit circle range
            return

        if event.button() == Qt.LeftButton:
            self.add_zero_or_pole(x, y)
        elif event.button() == Qt.RightButton:
            self.remove_closest_element(x, y)

    def add_zero_or_pole(self, x, y):
        """Add zero or pole and optionally its conjugate."""
        is_zero = self.zeros_radio_button.isChecked()
        is_pole = self.poles_radio_button.isChecked()
        if not (is_zero or is_pole):
            return

        target_list = self.zeros if is_zero else self.poles
        target_list.append(complex(x, y))

        # Add conjugate if checkbox is checked
        if self.add_conjugate_checkbox.isChecked() and y != 0:
            target_list.append(complex(x, -y))

        self.save_state()
        self.update_plot()

    def remove_closest_element(self, x, y):
        """Remove the closest zero or pole."""
        all_elements = self.zeros + self.poles
        if not all_elements:
            return

        closest = min(all_elements, key=lambda z: abs(z - complex(x, y)))
        if closest in self.zeros:
            self.zeros.remove(closest)
        elif closest in self.poles:
            self.poles.remove(closest)

        self.save_state()
        self.update_plot()

    def get_filter_coefficients(self):
        """Get filter coefficients from the current zeros and poles."""
        if not (self.zeros or self.poles):
            return [1], [1]  # Default: No filtering
        b = np.poly(self.zeros)  # Numerator coefficients
        a = np.poly(self.poles)  # Denominator coefficients
        return b, a

    def save_state(self):
        """Save the current state for undo/redo functionality."""
        self.history.append((self.zeros[:], self.poles[:]))
        self.redo_stack.clear()

    def undo(self):
        """Undo the last operation."""
        if not self.history:
            return
        self.redo_stack.append((self.zeros[:], self.poles[:]))
        self.zeros, self.poles = self.history.pop()
        self.update_plot()

    def redo(self):
        """Redo the last undone operation."""
        if not self.redo_stack:
            return
        self.history.append((self.zeros[:], self.poles[:]))
        self.zeros, self.poles = self.redo_stack.pop()
        self.update_plot()

    def clear_zeros(self):
        """Clear all zeros."""
        self.zeros.clear()
        self.save_state()
        self.update_plot()

    def clear_poles(self):
        """Clear all poles."""
        self.poles.clear()
        self.save_state()
        self.update_plot()

    def clear_all(self):
        """Clear all zeros and poles."""
        self.zeros.clear()
        self.poles.clear()
        self.save_state()
        self.update_plot()

    def save_to_file(self):
        """Save zeros and poles to a CSV file with a user-specified name and directory."""
        # Initialize Tkinter and hide the root window
        root = Tk()
        root.withdraw()

        # Prompt user to choose a file location and name
        filepath = asksaveasfilename(
            title="Save Filter Data",
            filetypes=[("CSV Files", "*.csv")],
            defaultextension=".csv"
        )

        # Exit if the user cancels the dialog
        if not filepath:
            return

        # Save zeros and poles to the selected file
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Real", "Imaginary"])
            for z in self.zeros:
                writer.writerow(["Zero", z.real, z.imag])
            for p in self.poles:
                writer.writerow(["Pole", p.real, p.imag])

        print(f"Filter data successfully saved to {filepath}")

    def load_from_file(self):
        """Load zeros and poles from a user-selected CSV file."""
        # Initialize Tkinter and hide the root window
        root = Tk()
        root.withdraw()

        # Prompt user to choose a file to load
        filepath = askopenfilename(
            title="Load Filter Data",
            filetypes=[("CSV Files", "*.csv")]
        )

        # Exit if the user cancels the dialog
        if not filepath:
            return

        # Check if the file exists
        if not os.path.exists(filepath):
            print(f"Error: File {filepath} does not exist.")
            return

        # Load zeros and poles from the selected file
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            self.zeros.clear()
            self.poles.clear()
            for row in reader:
                if row[0] == "Zero":
                    self.zeros.append(complex(float(row[1]), float(row[2])))
                elif row[0] == "Pole":
                    self.poles.append(complex(float(row[1]), float(row[2])))

        # Update application state and visuals
        self.save_state()
        self.update_plot()
        print(f"Filter data successfully loaded from {filepath}")

    def swap_zeros_poles(self):
        """Swap zeros and poles."""
        self.zeros, self.poles = self.poles, self.zeros
        self.save_state()
        self.update_plot()

    # def draw_direct_form_i_diagram(self):
    #     """Draw Direct Form I realization using SchemDraw."""
    #     # Get filter coefficients
    #     b_coeffs, a_coeffs = self.get_filter_coefficients()
    #
    #     # Normalize coefficients if a[0] != 1
    #     if a_coeffs[0] != 1:
    #         b_coeffs = b_coeffs / a_coeffs[0]
    #         a_coeffs = a_coeffs / a_coeffs[0]
    #
    #     # Start drawing the circuit
    #     with schemdraw.Drawing() as d:
    #         d.config(unit=1.5)  # Set unit scale for spacing
    #
    #         # Input
    #         d += elm.SourceV().label("x[n]", loc='left')
    #
    #         # Feedforward Path (b-coefficients)
    #         prev_block = None
    #         for i, b in enumerate(b_coeffs):
    #             if i > 0:
    #                 # Add delay blocks (z⁻¹)
    #                 d += elm.Dot() if prev_block is None else prev_block
    #                 d += elm.Line().down()
    #                 d += elm.Rect(w=1, h=0.5).label("Z⁻¹", loc='center')
    #                 prev_block = elm.Line().up()
    #             # Add feedforward coefficient block
    #             d += elm.Rect(w=1, h=0.5).label(f"b{i}={b:.2f}", loc='right')
    #
    #         # Summation Node
    #         d += elm.Dot(open=True).label("Σ", loc='center')
    #
    #         # Feedback Path (a-coefficients)
    #         for i, a in enumerate(a_coeffs[1:], start=1):  # Skip a[0] (assumed 1)
    #             d += elm.Line().down()
    #             d += elm.Rect(w=1, h=0.5).label("Z⁻¹", loc='center')
    #             d += elm.Rect(w=1, h=0.5).label(f"a{i}={a:.2f}", loc='right')
    #
    #         # Output
    #         d += elm.Line().right()
    #         d += elm.Dot(open=True).label("y[n]", loc='right')
    #
    #         # Save the diagram
    #         file_path = "direct_form_i_diagram.png"
    #         d.save(file_path)
    #
    #     return file_path

    def draw_direct_form_i_diagram(self):
        """Draw Direct Form I realization diagram horizontally using SchemDraw."""
        # Get filter coefficients
        b_coeffs, a_coeffs = self.get_filter_coefficients()

        # Normalize coefficients if a[0] != 1
        if a_coeffs[0] != 1:
            b_coeffs = b_coeffs / a_coeffs[0]
            a_coeffs = a_coeffs / a_coeffs[0]

        # Start drawing the circuit
        with schemdraw.Drawing() as d:
            d.config(unit=2)  # Set unit scale for spacing

            # Input signal
            d += elm.SourceV().label("x[n]", loc='left')

            # Summation node (Σ)
            summation = d.add(elm.Dot(open=True).label("Σ", loc="top"))

            # Feedforward path (b-coefficients)
            feedforward_anchor = summation  # Start from the summation node
            for i, b in enumerate(b_coeffs):
                if i > 0:
                    # Add delay block (Z⁻¹)
                    delay = d.add(elm.Rect(w=1.5, h=1).label("Z⁻¹", loc='center'))
                    d += elm.Line().right()  # Move to the next position
                # Add feedforward coefficient block
                d += elm.Rect(w=2, h=1).label(f"b{i}={b:.2f}", loc='center')

            # Feedback path (a-coefficients)
            for i, a in enumerate(a_coeffs[1:], start=1):  # Skip a[0] (assumed 1)
                d.push()  # Save current position
                d += elm.Line().down().length(2)  # Move down
                d += elm.Rect(w=1.5, h=1).label("Z⁻¹", loc='center')  # Add delay block
                d += elm.Line().left().length(4)  # Move left toward summation
                d += elm.Line().up().to(feedforward_anchor.center)  # Connect to the summation node
                d.pop()  # Restore position

            # Output signal
            d += elm.Line().right()
            d += elm.Rect(w=2, h=1).label("y[n]", loc='center')

            # Save the diagram
            file_path = "direct_form_i_horizontal_diagram.png"
            d.save(file_path)

        return file_path

    def display_circuit_in_groupbox(self):
        # Generate the diagram
        diagram_path = self.draw_direct_form_i_diagram()

        # Load the diagram into a QLabel
        pixmap = QPixmap(diagram_path)

        # Create a QLabel to hold the image
        diagram_label = QLabel()
        diagram_label.setPixmap(pixmap)
        diagram_label.setScaledContents(True)  # Scale the image to fit

        # Add the QLabel to the filter_realization_groupBox
        layout = QVBoxLayout(self.realization_plot)  # Assuming QVBoxLayout
        layout.addWidget(diagram_label)
        self.realization_plot.setLayout(layout)

