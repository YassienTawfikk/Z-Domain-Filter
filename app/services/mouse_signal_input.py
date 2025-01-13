from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget
import numpy as np
from pyqtgraph import mkPen
from scipy.signal import lfilter

class MouseSignalInput(QWidget):
    signal_generated = pyqtSignal(np.ndarray)  # Emitted when a new signal is generated

    def __init__(self, original_plot_widget, filtered_plot_widget, zplane_controller):
        super().__init__()
        self.original_plot_widget = original_plot_widget  # Widget to plot the original signal
        self.filtered_plot_widget = filtered_plot_widget  # Widget to plot the filtered signal
        self.zplane_controller = zplane_controller  # ZPlaneController for filter coefficients
        self.signal = []
        self.max_length = 10000  # Max signal length
        self.start_x, self.start_y = None, None
        self.current_filter = None  # Store the current filter
        self.window_length = 100  # Set the desired fixed length for the x-axis

        self.setMouseTracking(True)  # Enable mouse tracking without needing to click

    def mouseMoveEvent(self, event):
        """Capture mouse movement and generate signal."""
        if self.start_x is None:
            self.start_x, self.start_y = event.x(), event.y()

        dx = event.x() - self.start_x
        dy = event.y() - self.start_y

        # Generate the signal based on y-movement
        point = dy
        self.signal.append(point)

        # Keep the signal within the max length
        if len(self.signal) > self.max_length:
            self.signal.pop(0)

        # Define a fixed x-axis window length

        # Determine the x-axis range
        if len(self.signal) > self.window_length:
            x_min = len(self.signal) - self.window_length
            x_max = len(self.signal)
        else:
            x_min = 0
            x_max = self.window_length

        # Update the x-axis range
        self.original_plot_widget.setXRange(x_min, x_max, padding=0)

        # Plot the original signal
        self.original_plot_widget.plot(self.signal, clear=True, pen=mkPen("red"))

        # Filter the signal and plot the result
        self.apply_filter()

        # Emit the signal as a numpy array
        self.signal_generated.emit(np.array(self.signal))

    def set_filter(self, filter_name):
        """Set the current filter by name."""
        if filter_name in self.zplane_controller.filter_library:
            self.current_filter = self.zplane_controller.filter_library[filter_name]

    def apply_filter(self):
        """Apply the selected filter and plot the filtered signal."""
        if not self.signal:
            return

        # Convert the signal to float type
        float_signal = np.array(self.signal, dtype=np.float64)

        # Check for current filter
        if self.zplane_controller.filter_selection != "None":
            b, a = self.zplane_controller.filter_library[self.zplane_controller.filter_selection]()
        else:
            # Default to filter coefficients from ZPlaneController
            b, a = self.zplane_controller.get_filter_coefficients()

        # Apply the filter to the signal
        filtered_signal = lfilter(b, a, float_signal)
        filtered_signal = np.real(filtered_signal)  # Ensure the signal is real

        if len(filtered_signal) > self.window_length:
            x_min = len(filtered_signal) - self.window_length
            x_max = len(filtered_signal)
        else:
            x_min = 0
            x_max = self.window_length
        self.filtered_plot_widget.setXRange(x_min, x_max, padding=0)

        # Plot the filtered signal
        self.filtered_plot_widget.plot(filtered_signal, clear=True, pen=mkPen("green"))

    def reset(self):
        """Reset the signal and clear plots."""
        self.signal = []
        self.original_plot_widget.clear()
        self.filtered_plot_widget.clear()
        self.start_x = None
        self.start_y = None

