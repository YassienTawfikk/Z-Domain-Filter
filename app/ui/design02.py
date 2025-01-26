from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import mkBrush, mkColor
from PyQt5.QtWidgets import QComboBox ,QLineEdit

# ========== GLOBAL STYLESHEETS ==========
MAIN_WINDOW_STYLESHEET = """
    background-color: rgb(105, 132, 142);
    background-color: rgb(128, 144, 153);
"""

BUTTON_STYLESHEET = """
QPushButton {
    color: #fff;
    background-color: rgba(255, 255, 255, 0);
    border: 3px solid #fff;
    padding: 8px;
}
QPushButton:hover {
    background-color: rgba(255, 255, 255, 10);
}
"""

COMBOBOX_STYLESHEET = """
QComboBox {
    border: 2px solid #fff;
    padding: 1px;
}
"""

SPINBOX_STYLESHEET = """
QSpinBox {
    border: 2px solid #fff;
    padding: 1px;
    color: #000;
}
"""



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """
        Entry point to set up all UI components.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setStyleSheet(MAIN_WINDOW_STYLESHEET)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ---- 1. Top bar (Header) ----
        self.setupHeader()

        # ---- 2. Sidebar Layout ----
        self.setupSidebar()

        # ---- 3. Controls Layout (checkboxes, radio buttons, slider, etc.) ----
        self.setupControls()

        # ---- 4. Frequency Response Layout (group boxes) ----
        self.setupFrequencyResponse()

        # ---- 5. Z-Plane Layout (z-plane group box, filter realization, etc.) ----
        self.setupZPlane()

        MainWindow.setCentralWidget(self.centralwidget)

        # Menubar / Statusbar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Translations + finalize
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ----------------------------------------------------------------------
    # Below are the sub-methods that break down each UI section.
    # ----------------------------------------------------------------------
    def setupHeader(self):
        """
        Creates the top bar with the title, load/save filter buttons, and Quit button.
        """
        self.header_widget = QtWidgets.QWidget(self.centralwidget)
        self.header_widget.setGeometry(QtCore.QRect(10, 0, 1261, 41))
        self.header_widget.setStyleSheet("border: 1px solid #fff;")
        self.header_widget.setObjectName("header_widget")

        # Title
        self.app_title = QtWidgets.QLabel(self.header_widget)
        self.app_title.setGeometry(QtCore.QRect(0, 0, 221, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(29)
        self.app_title.setFont(font)
        self.app_title.setStyleSheet("color: white;")
        self.app_title.setObjectName("app_title")

        # Load Filter Button
        self.load_filter_button = QtWidgets.QPushButton(self.header_widget)
        self.load_filter_button.setGeometry(QtCore.QRect(260, 2, 125, 37))
        self.load_filter_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.load_filter_button.setFont(font)
        self.load_filter_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load_filter_button.setStyleSheet(BUTTON_STYLESHEET)
        self.load_filter_button.setObjectName("load_filter_button")

        # Save Filter Button
        self.save_filter_button = QtWidgets.QPushButton(self.header_widget)
        self.save_filter_button.setGeometry(QtCore.QRect(410, 2, 125, 37))
        self.save_filter_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.save_filter_button.setFont(font)
        self.save_filter_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_filter_button.setStyleSheet(BUTTON_STYLESHEET)
        self.save_filter_button.setObjectName("save_filter_button")

        # Combo Box
        self.filters_library_combobox = QtWidgets.QComboBox(self.header_widget)
        self.filters_library_combobox.setGeometry(QtCore.QRect(570, 8, 151, 27))
        self.filters_library_combobox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.filters_library_combobox.setStyleSheet(COMBOBOX_STYLESHEET)
        self.filters_library_combobox.setObjectName("filters_library_combobox")

        # Quit Button
        self.quit_button = QtWidgets.QPushButton(self.header_widget)
        self.quit_button.setGeometry(QtCore.QRect(1134, 2, 125, 37))
        self.quit_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.quit_button.setFont(font)
        self.quit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.quit_button.setStyleSheet(BUTTON_STYLESHEET)
        self.quit_button.setObjectName("quit_button")

    def setupSidebar(self):
        """
        Creates the vertical layout for the sidebar on the right side,
        including signal group boxes and any additional controllers.
        """
        # A vertical layout container for the sidebar
        self.sidebar_widget = QtWidgets.QWidget(self.centralwidget)
        self.sidebar_widget.setGeometry(QtCore.QRect(870, 50, 401, 721))
        self.sidebar_widget.setObjectName("sidebar_widget")

        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(20)

        # Mouse controller layout
        self.mouse_controller_layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(self.sidebar_widget)
        self.label.setMaximumSize(QtCore.QSize(285, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.mouse_controller_layout.addWidget(self.label)

        # “Padding area” inside
        self.padding_area = QtWidgets.QWidget(self.sidebar_widget)
        self.padding_area.setStyleSheet("""
            background-color: rgb(240, 240, 240);
            border-radius: 10px;
        """)
        self.padding_area.setObjectName("padding_area")
        self.padding_area.setMinimumSize(200, 200)
        self.mouse_controller_layout.addWidget(self.padding_area)

        self.sidebar_layout.addLayout(self.mouse_controller_layout)

        # Original signal groupbox
        self.original_signal_groupbox = QtWidgets.QGroupBox(self.sidebar_widget)
        self.original_signal_groupbox.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.original_signal_groupbox.setObjectName("original_signal_groupbox")
        self.sidebar_layout.addWidget(self.original_signal_groupbox)
        self.original_plot_widget = self.addGraphView(self.original_signal_groupbox)

        # Filtered signal groupbox
        self.filtered_signal_groupbox = QtWidgets.QGroupBox(self.sidebar_widget)
        self.filtered_signal_groupbox.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.filtered_signal_groupbox.setObjectName("filtered_signal_groupbox")
        self.sidebar_layout.addWidget(self.filtered_signal_groupbox)
        self.filtered_plot_widget = self.addGraphView(self.filtered_signal_groupbox)

    def setupControls(self):
        """
        Creates the ‘controls’ region with checkboxes, radio buttons, slider, etc.
        """
        self.controls_widget = QtWidgets.QWidget(self.centralwidget)
        self.controls_widget.setGeometry(QtCore.QRect(10, 399, 851, 61))
        self.controls_widget.setObjectName("controls_widget")

        # Checkboxes & RadioButtons
        self.add_conjugate_checkBox = QtWidgets.QCheckBox(self.controls_widget)
        self.add_conjugate_checkBox.setGeometry(QtCore.QRect(120, 20, 141, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.add_conjugate_checkBox.setFont(font)
        self.add_conjugate_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_conjugate_checkBox.setObjectName("add_conjugate_checkBox")

        self.zeros_radioButton = QtWidgets.QRadioButton(self.controls_widget)

        self.zeros_radioButton.setGeometry(QtCore.QRect(20, 10, 88, 19))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.zeros_radioButton.setFont(font)
        self.zeros_radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.zeros_radioButton.setObjectName("zeros_radioButton")

        self.poles_radioButton = QtWidgets.QRadioButton(self.controls_widget)
        self.poles_radioButton.setGeometry(QtCore.QRect(20, 32, 88, 19))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.poles_radioButton.setFont(font)
        self.poles_radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.poles_radioButton.setObjectName("poles_radioButton")
        # Grouping the first set of radio buttons
        self.zeros_poles_group = QtWidgets.QButtonGroup()
        self.zeros_poles_group.addButton(self.zeros_radioButton)
        self.zeros_poles_group.addButton(self.poles_radioButton)

        self.swap_button = QtWidgets.QPushButton(self.controls_widget)
        self.swap_button.setGeometry(QtCore.QRect(245, 12, 110, 37))
        self.swap_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.swap_button.setFont(font)
        self.swap_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.swap_button.setStyleSheet(BUTTON_STYLESHEET + "border-radius:10px;")
        self.swap_button.setObjectName("swap_button")

        self.all_pass_add_radioButton = QtWidgets.QRadioButton(self.controls_widget)
        self.all_pass_add_radioButton.setGeometry(QtCore.QRect(365, 10, 88, 19))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.all_pass_add_radioButton.setFont(font)
        self.all_pass_add_radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.all_pass_add_radioButton.setObjectName("all_pass_add_radioButton")

        self.all_pass_remove_radioButton = QtWidgets.QRadioButton(self.controls_widget)
        self.all_pass_remove_radioButton.setGeometry(QtCore.QRect(365, 32, 88, 19))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.all_pass_remove_radioButton.setFont(font)
        self.all_pass_remove_radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.all_pass_remove_radioButton.setObjectName("all_pass_remove_radioButton")

        # Input fields for custom zeros and poles
        self.custom_aribatry_input = QLineEdit(self.controls_widget)
        self.custom_aribatry_input.setGeometry(QtCore.QRect(485, 12, 110, 37))
        self.custom_aribatry_input.setPlaceholderText("Custom Zeros")
        self.custom_aribatry_input.setStyleSheet("QLineEdit { border: 2px solid #fff; }")



        self.create_button = QtWidgets.QPushButton(self.controls_widget)
        self.create_button.setGeometry(QtCore.QRect(725, 12, 110, 37))
        self.create_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.create_button.setFont(font)
        self.create_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.create_button.setStyleSheet(BUTTON_STYLESHEET + "border-radius:10px;")
        self.create_button.setObjectName("create_button")

    def setupFrequencyResponse(self):
        """
        Creates the horizontal layout for magnitude response & phase response group boxes.
        """
        self.frequency_response_widget = QtWidgets.QWidget(self.centralwidget)
        self.frequency_response_widget.setGeometry(QtCore.QRect(10, 460, 851, 311))
        self.frequency_response_widget.setObjectName("frequency_response_widget")

        self.frequency_response_layout = QtWidgets.QHBoxLayout(self.frequency_response_widget)
        self.frequency_response_layout.setContentsMargins(0, 0, 0, 0)
        self.frequency_response_layout.setSpacing(0)

        self.magnitude_response_groupbox = QtWidgets.QGroupBox(self.frequency_response_widget)
        self.magnitude_response_groupbox.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.magnitude_response_groupbox.setObjectName("magnitude_response_groupbox")
        self.frequency_response_layout.addWidget(self.magnitude_response_groupbox)
        self.magnitude_plot_widget = self.addGraphView(self.magnitude_response_groupbox)

        self.phase_response_groupbox = QtWidgets.QGroupBox(self.frequency_response_widget)
        self.phase_response_groupbox.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.phase_response_groupbox.setObjectName("phase_response_groupbox")
        self.phase_plot_widget = self.addGraphView(self.phase_response_groupbox)

        self.frequency_response_layout.addWidget(self.phase_response_groupbox)

    def setupZPlane(self):
        """
        Creates the z-plane area (left side plot and filter realization group box)
        along with the Clear/Undo/Redo buttons.
        """
        self.z_plane_widget = QtWidgets.QWidget(self.centralwidget)
        self.z_plane_widget.setGeometry(QtCore.QRect(11, 50, 849, 352))
        self.z_plane_widget.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.z_plane_widget.setObjectName("z_plane_widget")

        # select_all_pass_filters_button
        self.select_all_pass_filters_button = QtWidgets.QPushButton(self.z_plane_widget)
        self.select_all_pass_filters_button.setGeometry(QtCore.QRect(740, 30, 101, 40))
        self.select_all_pass_filters_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.select_all_pass_filters_button.setFont(font)
        self.select_all_pass_filters_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.select_all_pass_filters_button.setStyleSheet("""
                    QPushButton {
                        color: #809099;
                        background-color: rgba(255, 255, 255, 0);
                        border: 3px solid #809099;
                        padding: 3px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 70);
                    }
                """)
        self.select_all_pass_filters_button.setObjectName("clear_zeros_button")

        # Clear Zeros
        self.clear_zeros_button = QtWidgets.QPushButton(self.z_plane_widget)
        self.clear_zeros_button.setGeometry(QtCore.QRect(740, 90, 101, 40))
        self.clear_zeros_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.clear_zeros_button.setFont(font)
        self.clear_zeros_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clear_zeros_button.setStyleSheet("""
            QPushButton {
                color: #809099;
                background-color: rgba(255, 255, 255, 0);
                border: 3px solid #809099;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 70);
            }
        """)
        self.clear_zeros_button.setObjectName("clear_zeros_button")

        # Clear Poles
        self.clear_poles_button = QtWidgets.QPushButton(self.z_plane_widget)
        self.clear_poles_button.setGeometry(QtCore.QRect(740, 150, 101, 40))
        self.clear_poles_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.clear_poles_button.setFont(font)
        self.clear_poles_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clear_poles_button.setStyleSheet("""
            QPushButton {
                color: #809099;
                background-color: rgba(255, 255, 255, 0);
                border: 3px solid #809099;
                padding: 1px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 70);
            }
        """)
        self.clear_poles_button.setObjectName("clear_poles_button")

        # Clear All
        self.clear_all_button = QtWidgets.QPushButton(self.z_plane_widget)
        self.clear_all_button.setGeometry(QtCore.QRect(740, 210, 101, 40))
        self.clear_all_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.clear_all_button.setFont(font)
        self.clear_all_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clear_all_button.setStyleSheet("""
            QPushButton {
                color: rgb(255, 255, 255);
                background-color: #809099;
                padding: 3px;
            }
        """)
        self.clear_all_button.setObjectName("clear_all_button")

        # Undo
        self.undo_button = QtWidgets.QPushButton(self.z_plane_widget)
        self.undo_button.setGeometry(QtCore.QRect(721, 300, 59, 31))
        self.undo_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.undo_button.setFont(font)
        self.undo_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.undo_button.setStyleSheet("""
            QPushButton {
                color: #809099;
                background-color: rgba(255, 255, 255, 0);
                border: 3px solid #809099;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 10);
            }
        """)
        self.undo_button.setObjectName("undo_button")

        # Redo
        self.redo_button = QtWidgets.QPushButton(self.z_plane_widget)
        self.redo_button.setGeometry(QtCore.QRect(788, 300, 59, 31))
        self.redo_button.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.redo_button.setFont(font)
        self.redo_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.redo_button.setStyleSheet("""
            QPushButton {
                color: #809099;
                background-color: rgba(255, 255, 255, 0);
                border: 3px solid #809099;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 10);
            }
        """)
        self.redo_button.setObjectName("redo_button")

        # Z-plane group box
        self.z_plane_plot_groupbox = QtWidgets.QGroupBox(self.z_plane_widget)
        self.z_plane_plot_groupbox.setGeometry(QtCore.QRect(-1, 0, 350, 350))
        self.z_plane_plot_groupbox.setObjectName("z_plane_plot_groupbox")
        self.z_plane_plot_widget = self.addGraphView(self.z_plane_plot_groupbox)

        # Filter Realization group box
        self.filter_realization_groupBox = QtWidgets.QGroupBox(self.z_plane_widget)
        self.filter_realization_groupBox.setGeometry(QtCore.QRect(360, 0, 360, 350))
        self.filter_realization_groupBox.setTitle("")
        self.filter_realization_groupBox.setObjectName("filter_realization_groupBox")
        # self.filter_ralization_plot_widget = self.addGraphView(self.filter_realization_groupBox)

        # Filter Realization group box
        self.filter_realization_groupBox = QtWidgets.QGroupBox(self.z_plane_widget)
        self.filter_realization_groupBox.setGeometry(QtCore.QRect(360, 0, 360, 350))
        self.filter_realization_groupBox.setTitle("")
        self.filter_realization_groupBox.setObjectName("filter_realization_groupBox")

        # Filter Realization Buttons
        self.filter_realizaion_structure = QtWidgets.QPushButton(self.filter_realization_groupBox)
        self.filter_realizaion_structure.setGeometry(QtCore.QRect(10, 5, 84, 25))
        font = QtGui.QFont()
        font.setBold(True)
        self.filter_realizaion_structure.setFont(font)
        self.filter_realizaion_structure.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.filter_realizaion_structure.setStyleSheet("""
            QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgba(255, 255, 255, 0);
                border: 2px solid #809099;
                padding: 1px;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 70);
            }
        """)
        self.filter_realizaion_structure.setObjectName("filter_realizaion_structure")
        self.filter_realizaion_structure.setText("Structure")

        # self.filter_realization_code = QtWidgets.QPushButton(self.filter_realization_groupBox)
        # self.filter_realization_code.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # self.filter_realization_code.setGeometry(QtCore.QRect(100, 5, 84, 25))
        # self.filter_realization_code.setFont(font)
        # self.filter_realization_code.setStyleSheet("""
        #     QPushButton {
        #         color: rgb(0, 0, 0);
        #         background-color: rgba(255, 255, 255, 0);
        #         border: 2px solid #809099;
        #         padding: 1px;
        #         border-radius: 7px;
        #     }
        #     QPushButton:hover {
        #         background-color: rgba(255, 255, 255, 70);
        #     }
        # """)
        # self.filter_realization_code.setObjectName("filter_realization_code")
        # self.filter_realization_code.setText("Code")

        # Label for Diagram
        self.filter_realization_diagram_label = QtWidgets.QLabel(self.filter_realization_groupBox)
        self.filter_realization_diagram_label.setGeometry(QtCore.QRect(10, 40, 340, 300))  # Adjust position and size
        self.filter_realization_diagram_label.setStyleSheet("""
            QLabel {
                border-radius: 7px;
                background-color: rgba(255, 255, 255, 50);
            }
        """)
        self.filter_realization_diagram_label.setObjectName("filter_realization_diagram_label")
        # self.filter_realization_diagram_label.setText("Filter Realization Diagram")
        self.filter_realization_diagram_label.setAlignment(QtCore.Qt.AlignCenter)

    def addGraphView(self, group_box):
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground((240, 240, 240, 0.5))
        plot_widget.showGrid(x=True, y=True, alpha=0.5)

        graph_layout = QtWidgets.QVBoxLayout()
        graph_layout.addWidget(plot_widget)
        group_box.setLayout(graph_layout)
        group_box.setMaximumSize(500, 350)
        plot_widget.setGeometry(group_box.rect())

        return plot_widget


    # ----------------------------------------------------------------------
    # Translating texts, labels, etc.
    # ----------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # Header
        self.app_title.setText(_translate("MainWindow", "Digital Filter"))
        self.load_filter_button.setText(_translate("MainWindow", "Load Filter"))
        self.save_filter_button.setText(_translate("MainWindow", "Save Filter"))
        self.quit_button.setText(_translate("MainWindow", "Quit App"))

        # Sidebar
        self.label.setText(_translate("MainWindow", "Move your mouse here to generate signal"))
        self.original_signal_groupbox.setTitle(_translate("MainWindow", "Original Signal"))
        self.filtered_signal_groupbox.setTitle(_translate("MainWindow", "Filtered Signal"))

        # Controls
        self.add_conjugate_checkBox.setText(_translate("MainWindow", "Add Conjugate"))
        self.zeros_radioButton.setText(_translate("MainWindow", "Zeros"))
        self.poles_radioButton.setText(_translate("MainWindow", "Poles"))
        self.swap_button.setText(_translate("MainWindow", "Swap"))
        self.create_button.setText(_translate("MainWindow", "Create"))
        self.all_pass_add_radioButton.setText(_translate("MainWindow", "apAdd"))
        self.all_pass_remove_radioButton.setText(_translate("MainWindow", "apRemove"))


        # Frequency Response
        self.magnitude_response_groupbox.setTitle(_translate("MainWindow", "Magnitude Response"))
        self.phase_response_groupbox.setTitle(_translate("MainWindow", "Phase Response"))

        # Z-plane
        self.clear_zeros_button.setText(_translate("MainWindow", "Clear Zero"))
        self.select_all_pass_filters_button.setText(_translate("MainWindow", "All Pass"))
        self.clear_poles_button.setText(_translate("MainWindow", "Clear Pole"))
        self.clear_all_button.setText(_translate("MainWindow", "Clear ALL"))
        self.undo_button.setText(_translate("MainWindow", "Undo"))
        self.redo_button.setText(_translate("MainWindow", "Redo"))
        self.z_plane_plot_groupbox.setTitle(_translate("MainWindow", "Z Plane"))
        self.filter_realizaion_structure.setText(_translate("MainWindow", "Structure"))
        # self.filter_realization_code.setText(_translate("MainWindow", "Code"))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
