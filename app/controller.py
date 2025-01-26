from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout

from app.services.mouse_signal_input import MouseSignalInput
from app.services.zplane_controller import ZPlaneController
from app.ui.design02 import Ui_MainWindow
from app.utils.clean_cache import remove_directories


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initialize_z_plane()
        self.initialize_mouse_signal_input()
        # self.zplane_controller.export_filter_to_c()

        self.connect_signals()

    def initialize_z_plane(self):
        # Initialize ZPlaneController
        self.zplane_controller = ZPlaneController(
            self.ui.z_plane_plot_widget,
            self.ui.magnitude_plot_widget,
            self.ui.phase_plot_widget,
            self.ui.filter_realization_diagram_label,
            self.ui.add_conjugate_checkBox,
            self.ui.zeros_radioButton,
            self.ui.poles_radioButton,
            self.ui.custom_aribatry_input,
            self.ui.all_pass_remove_radioButton,
            self.ui.all_pass_add_radioButton,
            self.ui.select_all_pass_filters_button,
            self.ui.create_button
        )

    def initialize_mouse_signal_input(self):
        """Set up the mouse signal generator."""
        self.original_plot_widget = self.ui.original_plot_widget  # Plot to display the signal
        self.mouse_signal_input = MouseSignalInput(self.original_plot_widget, self.ui.filtered_plot_widget, self.zplane_controller,self.ui.all_pass_add_radioButton,self.ui.all_pass_remove_radioButton)

        # Embed the MouseSignalInput into the padding_area
        self.padding_area_layout = QVBoxLayout(self.ui.padding_area)
        self.padding_area_layout.addWidget(self.mouse_signal_input)

    def connect_signals(self):
        self.ui.quit_button.clicked.connect(self.quit_app)
        #self.ui.horizontalSlider.valueChanged.connect(self.ui.update_slider_label)

        self.ui.save_filter_button.clicked.connect(lambda: self.zplane_controller.save_to_file())
        self.ui.load_filter_button.clicked.connect(lambda: self.zplane_controller.load_from_file())

        # Connect Z-plane actions
        self.ui.swap_button.clicked.connect(self.zplane_controller.swap_zeros_poles)
        self.ui.clear_zeros_button.clicked.connect(self.zplane_controller.clear_zeros)
        self.ui.clear_poles_button.clicked.connect(self.zplane_controller.clear_poles)
        self.ui.clear_all_button.clicked.connect(self.zplane_controller.clear_all)
        self.ui.undo_button.clicked.connect(self.zplane_controller.undo)
        self.ui.redo_button.clicked.connect(self.zplane_controller.redo)
        # Populate the combobox with filters
        self.ui.filters_library_combobox.addItems(self.zplane_controller.filter_library.keys())
        self.ui.filters_library_combobox.currentIndexChanged.connect(self.apply_selected_filter)
        self.ui.filter_realizaion_structure.clicked.connect(self.zplane_controller.display_circuit_in_groupbox)
        self.zplane_controller.configure_x_axis(self.ui.magnitude_plot_widget)
        self.zplane_controller.configure_x_axis(self.ui.phase_plot_widget)

    def apply_selected_filter(self, index):
        """Handle filter selection from the combobox."""
        if index < 0:
            return  # Ignore invalid selection
        filter_name = self.ui.filters_library_combobox.itemText(index)
        self.zplane_controller.filter_selection = filter_name
        self.zplane_controller.update_z_plane_from_filter()  # Update Z-plane
        self.mouse_signal_input.set_filter(filter_name)

    def quit_app(self):
        self.app.quit()
        remove_directories()
