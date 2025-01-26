import csv
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import numpy as np
from pyqtgraph import mkPen
from pyqtgraph.examples.glow import update_plot
from scipy.signal import butter, cheby1, cheby2, ellip, freqz
import schemdraw
import schemdraw.elements as elm
import schemdraw.flow as flow  # Use the flow module for box elements

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5 import QtWidgets


class ZPlaneController:
    def __init__(self, plot_widget, mag_plot_widget, phase_plot_widget, realization_plot, add_conjugate_checkbox, zeros_radio_button, poles_radio_button,custom_aribatry_input,all_pass_remove_radioButton,all_pass_add_radioButton,select_all_pass_filters_button,create_button):
        self.plot_widget = plot_widget
        self.add_conjugate_checkbox = add_conjugate_checkbox
        self.zeros_radio_button = zeros_radio_button
        self.poles_radio_button = poles_radio_button
        self.mag_plot_widget = mag_plot_widget
        self.phase_plot_widget = phase_plot_widget
        self.realization_plot = realization_plot
        self.custom_aribatry_input = custom_aribatry_input
        self.all_pass_remove_radioButton = all_pass_remove_radioButton
        self.all_pass_add_radioButton =all_pass_add_radioButton
        self.select_all_pass_filters_button =select_all_pass_filters_button
        self.create_button = create_button

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

            # Chebyshev I Filter
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

        # All-pass filter library
        self.all_pass_filter_library = {
            "All-Pass 1": {'zeros': [-2], 'poles': [-0.5]},
            "All-Pass 2": {'zeros': [1/0.8], 'poles': [0.8]},
            "All-Pass 3": {'zeros': [-2-1j], 'poles': [1/(-2+1j)]},
            "All-Pass 4": {'zeros': [2j], 'poles': [1 / (-2j)]},
        }

        self.selected_all_pass_filters = []

        self.select_all_pass_filters_button.clicked.connect(self.openFilterPopup)
        self.create_button.clicked.connect(self.add_custom_all_pass_filter)

        self.all_pass_add_radioButton.toggled.connect(self.update_plot)
        self.all_pass_remove_radioButton.toggled.connect(self.update_plot)

    def openFilterPopup(self):
        # Create a new dialog
        self.filter_dialog = QtWidgets.QDialog()
        self.filter_dialog.setWindowTitle("Select Filters")
        self.filter_dialog.setGeometry(100, 100, 300, 400)

        # Layout for the dialog
        layout = QtWidgets.QVBoxLayout()

        # Sample filter options (you can replace these with your actual filters)
        filters = self.all_pass_filter_library

        # Create checkboxes for each filter
        self.filter_checkboxes = {}
        for filter_name in filters:
            checkbox = QtWidgets.QCheckBox(filter_name)
            self.filter_checkboxes[filter_name] = checkbox
            layout.addWidget(checkbox)

        # Add OK button to the dialog
        ok_button = QtWidgets.QPushButton("OK")
        ok_button.clicked.connect(self.applyFilters)
        layout.addWidget(ok_button)

        self.filter_dialog.setLayout(layout)
        self.filter_dialog.exec_()

    def applyFilters(self):
        self.selected_all_pass_filters = [self.all_pass_filter_library[filter_name] for filter_name, checkbox in self.filter_checkboxes.items() if
                            checkbox.isChecked()]
        print("Selected Filters:", self.selected_all_pass_filters)  # Process the selected filters as needed
        self.all_pass_add_radioButton.click()
        self.update_plot()
        self.filter_dialog.close()

    def add_custom_all_pass_filter(self):
        a = self.custom_aribatry_input.text().split(',')

        # Filter out empty strings and convert to complex numbers
        zeros = [complex(float(z.strip())) for z in a if z.strip()]
        conjugates = np.conjugate(zeros)
        poles = 1/conjugates

        self.selected_all_pass_filters=[{'zeros': zeros, 'poles': poles}]
        self.all_pass_add_radioButton.click()
        self.update_plot()
        self.all_pass_filter_library["Custom"] ={'zeros': zeros, 'poles': poles}
        self.custom_aribatry_input.clear()
        print("Selected Filters:", self.selected_all_pass_filters)


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

        if self.all_pass_add_radioButton.isChecked():
            b = np.poly(self.combined_zeros)  # Numerator coefficients
            a = np.poly(self.combined_poles)  # Numerator coefficients
        else:
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
        # Start with the current filter's zeros and poles
        self.combined_zeros = self.zeros.copy()
        self.combined_poles = self.poles.copy()
        if self.all_pass_add_radioButton.isChecked():

            # Include selected all-pass filters
            for filter in self.selected_all_pass_filters:
                self.combined_zeros.extend(filter['zeros'])
                self.combined_poles.extend(filter['poles'])

        self.scatter_zeros.setData([z.real for z in self.combined_zeros], [z.imag for z in self.combined_zeros])
        self.scatter_poles.setData([p.real for p in self.combined_poles], [p.imag for p in self.combined_poles])
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
        if self.all_pass_add_radioButton.isChecked:
            b = np.poly(self.combined_zeros)  # Numerator coefficients
            a = np.poly(self.combined_poles)  # Denominator coefficients
        else:
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

    def draw_direct_form_ii_diagram(self):
        """Draw Direct Form II realization using SchemDraw."""

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
            d.add(elm.SourceV().label("x[n]", loc='left'))  # x_in

            # First Summation Node (Input to Feedforward and Feedback Paths)
            sum_node1 = d.add(elm.Dot(open=True).label("Σ", loc='center'))

            # Feedforward Path (b-coefficients)
            current = sum_node1
            for i, b in enumerate(b_coeffs):
                # d.add(elm.Rect(w=2, h=1).label(f"b{i}={b:.2f}", loc='center')) #coeff_block
                # d.add(elm.Line().down().length(1.5))

                d.add(elm.Line(w=1, h=1).label(f"b{i}={b:.2f}", loc='center'))
                if i == 0:
                    d.add(elm.Dot(open=True).label("y[n]", loc='center')) #output

            # Feedback Path (a-coefficients)
            current = sum_node1
            delay_blocks = []

            for i, a in enumerate(a_coeffs[1:], start=1):  # Skip a[0] (assumed 1)
                d.add(elm.Line().down().length(1.5))
                delay = d.add(elm.Rect(w=2, h=1).label("Z⁻¹", loc='center'))
                delay_blocks.append(delay)
                d.add(elm.Line().left().length(1.5))
                # d.add(elm.Rect(w=2, h=1).label(f"a{i}={a:.2f}", loc='center'))
                d.add(elm.Line(w=2, h=1).label(f"a{i}={a:.2f}", loc='center'))

            # Shared Delay Line (Z⁻¹ blocks)
            shared_delay_start = sum_node1
            for _ in range(max(len(a_coeffs), len(b_coeffs)) - 1):
                d.add(elm.Line().down().length(2))
                d.add(elm.Rect(w=2, h=1).label("Z⁻¹", loc='center'))
                d.add(elm.Line().down().length(2).at(shared_delay_start.end))

            # Save the diagram
            file_path = "static/images/direct_form_ii_diagram.png"
            d.save(file_path)

        return file_path

    def display_circuit_in_groupbox(self):
        """Display the generated circuit diagram in a PyQt GroupBox."""
        # Generate the diagram
        diagram_path = self.draw_direct_form_ii_diagram()

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
