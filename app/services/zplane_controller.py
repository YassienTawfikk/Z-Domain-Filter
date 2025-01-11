from pyqtgraph import PlotWidget, mkPen
from scipy import signal
from scipy.signal import freqz, butter, cheby1, cheby2, ellip, sosfreqz,lfilter ,tf2sos
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import numpy as np
import csv
import os
# from tkinter import Tk
# from tkinter.filedialog import asksaveasfilename, askopenfilename


class ZPlaneController:
    def __init__(self, plot_widget ,mag_plot_widget, phase_plot_widget, add_conjugate_checkbox, zeros_radio_button, poles_radio_button):
        self.plot_widget = plot_widget
        self.add_conjugate_checkbox = add_conjugate_checkbox
        self.zeros_radio_button = zeros_radio_button
        self.poles_radio_button = poles_radio_button
        self.mag_plot_widget = mag_plot_widget
        self.phase_plot_widget = phase_plot_widget

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
        self.ax_h = self.plot_widget.plot([-1, 1], [0, 0], pen=mkPen('blue', width=2))  # Horizontal axis (x-axis)
        self.ax_v = self.plot_widget.plot([0, 0], [-1, 1], pen=mkPen('blue', width=2))  # Vertical axis (y-axis)

        self.update_unit_circle()
        # Frequency response plots
        self.mag_response = self.mag_plot_widget.plot(pen=mkPen("green"))
        self.phase_response = self.phase_plot_widget.plot(pen=mkPen("red"))

        # Signal connections
        self.plot_widget.scene().sigMouseClicked.connect(self.on_mouse_click)

        # Filter library
        self.filter_library = {
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

        # Connect filter selection
        self.filter_selection = None  # Store selected filter

    # def apply_selected_filter(self):
    #     """Apply the selected filter to the input signal."""
    #     if self.filter_selection:
    #         b, a = self.filter_library[self.filter_selection]()
    #         # Apply the filter to the input signal (assumed to be available)
    #         filtered_signal = lfilter(b, a, self.input_signal)
    #         return filtered_signal

    def on_filter_selection_changed(self, index):
        """Handle filter selection change."""
        self.filter_selection = list(self.filter_library.keys())[index]

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
        self.mag_response.setData(w, np.abs(h))
        self.phase_response.setData(w, np.angle(h))

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
        # root = Tk()
        # root.withdraw()

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
        # root = Tk()
        # root.withdraw()

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


