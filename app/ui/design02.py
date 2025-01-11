from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import mkBrush, mkColor
from PyQt5.QtWidgets import QComboBox

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

SLIDER_STYLESHEET = """
QSlider::groove:horizontal {
    border: 1px solid #1D2731;
    height: 8px;
    background: #fff;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #00aaff;
    border: 2px solid #005f87; 
    width: 16px;
    height: 16px;
    border-radius: 8px;
    margin: -4px 0;
}
QSlider::sub-page:horizontal {
    background: #00aaff;
    border-radius: 4px;
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

        # Slider
        self.horizontalSlider = QtWidgets.QSlider(self.controls_widget)
        self.horizontalSlider.setGeometry(QtCore.QRect(270, 20, 261, 21))
        self.horizontalSlider.setStyleSheet(SLIDER_STYLESHEET)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setValue(50)

        self.percentage = QtWidgets.QLabel(self.controls_widget)
        self.percentage.setGeometry(QtCore.QRect(540, 18, 45, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.percentage.setFont(font)
        self.percentage.setStyleSheet("color: black;")
        self.percentage.setObjectName("percentage")

        # All Pass Filters
        self.all_pass_filters = QtWidgets.QPushButton(self.controls_widget)
        self.all_pass_filters.setGeometry(QtCore.QRect(630, 12, 181, 37))
        self.all_pass_filters.setMaximumSize(QtCore.QSize(240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.all_pass_filters.setFont(font)
        self.all_pass_filters.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.all_pass_filters.setStyleSheet(BUTTON_STYLESHEET + "border-radius:10px;")
        self.all_pass_filters.setObjectName("all_pass_filters")

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

        # Filter Realization Buttons
        self.filter_realizaion_structure = QtWidgets.QPushButton(self.filter_realization_groupBox)
        self.filter_realizaion_structure.setGeometry(QtCore.QRect(10, 5, 84, 25))
        font = QtGui.QFont()
        font.setBold(True)
        self.filter_realizaion_structure.setFont(font)
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

        self.filter_realizaion_code = QtWidgets.QPushButton(self.filter_realization_groupBox)
        self.filter_realizaion_code.setGeometry(QtCore.QRect(100, 5, 84, 25))
        font = QtGui.QFont()
        font.setBold(True)
        self.filter_realizaion_code.setFont(font)
        self.filter_realizaion_code.setStyleSheet("""
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
        self.filter_realizaion_code.setObjectName("filter_realizaion_code")

        # Built-in library combo box
        self.built_In_library_comboBox = QtWidgets.QComboBox(self.z_plane_widget)
        self.built_In_library_comboBox.setGeometry(QtCore.QRect(730, 10, 111, 25))
        self.built_In_library_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.built_In_library_comboBox.setStyleSheet("""
            QComboBox {
                color: rgb(0, 0, 0);
                background-color: rgba(255, 255, 255, 0);
                border: 2px solid #809099;
                padding: 1px;
                border-radius: 7px;
            }
        """)
        self.built_In_library_comboBox.setObjectName("built_In_library_comboBox")

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

    def update_slider_label(self):
        self.percentage.setText(f"{self.horizontalSlider.value()}%")

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
        self.percentage.setText(_translate("MainWindow", "50%"))
        self.all_pass_filters.setText(_translate("MainWindow", "All Pass Filters"))

        # Frequency Response
        self.magnitude_response_groupbox.setTitle(_translate("MainWindow", "Magnitude Response"))
        self.phase_response_groupbox.setTitle(_translate("MainWindow", "Phase Response"))

        # Z-plane
        self.clear_zeros_button.setText(_translate("MainWindow", "Clear Zero"))
        self.clear_poles_button.setText(_translate("MainWindow", "Clear Pole"))
        self.clear_all_button.setText(_translate("MainWindow", "Clear ALL"))
        self.undo_button.setText(_translate("MainWindow", "Undo"))
        self.redo_button.setText(_translate("MainWindow", "Redo"))
        self.z_plane_plot_groupbox.setTitle(_translate("MainWindow", "Z Plane"))
        self.filter_realizaion_structure.setText(_translate("MainWindow", "Structure"))
        self.filter_realizaion_code.setText(_translate("MainWindow", "Code"))


# class Ui_MainWindow(object):
#
#     # -----------------------
#     # Create/Helper Methods
#     # -----------------------
#     def createHorizontalLayout(self, parent, x, y, width, height):
#         widget = QtWidgets.QWidget(parent)
#         widget.setGeometry(QtCore.QRect(x, y, width, height))
#         layout = QtWidgets.QHBoxLayout(widget)
#         layout.setContentsMargins(0, 0, 0, 0)
#         widget.setObjectName(f"horizontalLayoutWidget_{x}_{y}")
#         return layout
#
#     def createVerticalLayout(self, parent, x, y, width, height):
#         widget = QtWidgets.QWidget(parent)
#         widget.setGeometry(QtCore.QRect(x, y, width, height))
#         layout = QtWidgets.QVBoxLayout(widget)
#         layout.setContentsMargins(0, 0, 0, 0)
#         widget.setObjectName(f"verticalLayoutWidget_{x}_{y}")
#         return layout
#
#     def createLabel(self, layout, text="", pixmap=None, max_size=50, text_font=None, isVisible=True, color="white"):
#         label = QtWidgets.QLabel(layout.parent())
#         if pixmap:
#             label.setPixmap(QtGui.QPixmap(pixmap))
#             label.setScaledContents(True)
#         if text_font:
#             font = QtGui.QFont()
#             font.setFamily(text_font[0])
#             font.setPointSize(text_font[1])
#             label.setFont(font)
#         if text:
#             label.setText(text)
#         label.setStyleSheet(f"color: {color};")
#         # If you want to allow different widths & heights, adjust as needed:
#         if isinstance(max_size, int):
#             label.setMaximumSize(QtCore.QSize(max_size, max_size))
#         else:
#             label.setMaximumSize(QtCore.QSize(*max_size))
#         layout.addWidget(label)
#         if not isVisible:
#             label.hide()
#         return label
#
#     def createButton(self, layout, text, stylesheet=BUTTON_STYLESHEET, method=None, isVisible=True, max_size=(150, 40)):
#         button = QtWidgets.QPushButton(layout.parent())
#         button.setText(text)
#         button.setObjectName(f"{text.lower().replace(' ', '_')}_button")
#         button.setMaximumSize(QtCore.QSize(*max_size))
#         button.setMinimumSize(QtCore.QSize(*max_size))
#         button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
#         button.setStyleSheet(stylesheet)
#         if method:
#             button.clicked.connect(method)
#         layout.addWidget(button)
#         if not isVisible:
#             button.hide()
#         return button
#
#     def createSlider(self, layout, min_value=0, max_value=100, initial_value=50,
#                      orientation=QtCore.Qt.Horizontal, isVisible=True, stylesheet=SLIDER_STYLESHEET):
#         slider_layout = QtWidgets.QHBoxLayout()
#         slider_layout.setContentsMargins(0, 0, 0, 0)
#         slider_layout.setSpacing(10)
#
#         slider = QtWidgets.QSlider(orientation, layout.parent())
#         slider.setMinimum(min_value)
#         slider.setMaximum(max_value)
#         slider.setValue(initial_value)
#         slider.setMaximumWidth(200)
#         slider.setStyleSheet(stylesheet)
#         if not isVisible:
#             slider.hide()
#
#         slider_layout.addWidget(slider)
#         layout.addLayout(slider_layout)
#
#         return slider
#
#     def createSpinBox(self, layout, min_value=0, max_value=100, initial_value=50,
#                       stylesheet=SPINBOX_STYLESHEET, isVisible=True):
#         spin_box = QtWidgets.QSpinBox(layout.parent())
#         spin_box.setMinimum(min_value)
#         spin_box.setMaximum(max_value)
#         spin_box.setValue(initial_value)
#         spin_box.setMaximumSize(260, 40)
#         spin_box.setStyleSheet(stylesheet)
#         if not isVisible:
#             spin_box.hide()
#
#         layout.addWidget(spin_box)
#         return spin_box
#
#     def createComboBox(self, layout, options, default_value=None, isEditable=False,
#                        isVisible=True, initial_index=0, stylesheet=COMBOBOX_STYLESHEET):
#         combo_box = QtWidgets.QComboBox(layout.parent())
#         combo_box.addItems(options)
#         combo_box.setEditable(isEditable)
#         combo_box.setMaximumSize(260, 40)
#         combo_box.setStyleSheet(stylesheet)
#
#         if 0 <= initial_index < len(options):
#             combo_box.setCurrentIndex(initial_index)
#
#         if not isVisible:
#             combo_box.hide()
#
#         layout.addWidget(combo_box)
#         return combo_box
#
#     # -----------------------------------------------------------
#     # Main setupUi
#     # -----------------------------------------------------------
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(1280, 800)
#         MainWindow.setStyleSheet(MAIN_WINDOW_STYLESHEET)
#
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#
#         # 1. Header
#         self.setupHeader()
#
#         # 2. Sidebar
#         self.setupSidebar()
#
#         # 3. Controls area
#         self.setupControls()
#
#         # 4. Frequency Response
#         self.setupFrequencyResponse()
#
#         # 5. Z-plane
#         self.setupZPlane()
#
#         # Set central widget, menubar, statusbar
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 25))
#         MainWindow.setMenuBar(self.menubar)
#
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#     # -----------------------------------------------------------
#     # Sub-sections
#     # -----------------------------------------------------------
#     def setupHeader(self):
#         """
#         Header bar: we create a horizontal layout and place
#         Title, Load Filter, Save Filter, ComboBox, Quit Button inside.
#         """
#         # Create a horizontal layout
#         header_layout = self.createHorizontalLayout(self.centralwidget, 10, 0, 1261, 41)
#         header_layout.parent().setStyleSheet("border: 1px solid #fff;")
#         header_layout.parent().setObjectName("header_widget")
#
#         # Title
#         self.app_title = self.createLabel(
#             header_layout, text="Digital Filter", text_font=("Arial", 29), max_size=(300, 50), color="white"
#         )
#
#         # Load Filter Button
#         self.load_filter_button = self.createButton(
#             header_layout, "Load Filter", BUTTON_STYLESHEET
#         )
#
#         # Save Filter Button
#         self.save_filter_button = self.createButton(
#             header_layout, "Save Filter", BUTTON_STYLESHEET
#         )
#
#         # Combobox
#         self.comboBox_2 = QtWidgets.QComboBox(header_layout.parent())
#         self.comboBox_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
#         self.comboBox_2.setStyleSheet(COMBOBOX_STYLESHEET)
#         header_layout.addWidget(self.comboBox_2)
#
#         # Quit Button
#         self.quit_button = self.createButton(
#             header_layout, "Quit App", BUTTON_STYLESHEET
#         )
#
#     def setupSidebar(self):
#         """
#         Sidebar on the right side with a vertical layout, containing:
#         - Mouse controller label
#         - A 'padding_area' widget
#         - Original signal groupbox
#         - Filtered signal groupbox
#         """
#         # Create the sidebar vertical layout
#         sidebar_layout = self.createVerticalLayout(self.centralwidget, 870, 50, 401, 721)
#         sidebar_layout.parent().setObjectName("sidebar_widget")
#         sidebar_layout.setSpacing(20)
#
#         # (1) Mouse controller label
#         mouse_controller_layout = QtWidgets.QVBoxLayout()
#         # Label
#         self.label = self.createLabel(
#             mouse_controller_layout,
#             text="Move your mouse here to generate signal",
#             text_font=("Arial", 11),
#             max_size=(285, 20),
#             color="white"
#         )
#         # Padding area
#         self.padding_area = QtWidgets.QWidget(sidebar_layout.parent())
#         self.padding_area.setStyleSheet("""
#             background-color: rgb(240, 240, 240);
#             border-radius: 10px;
#         """)
#         mouse_controller_layout.addWidget(self.padding_area)
#
#         sidebar_layout.addLayout(mouse_controller_layout)
#
#         # (2) Original signal groupbox
#         self.original_signal_groupbox = QtWidgets.QGroupBox(sidebar_layout.parent())
#         self.original_signal_groupbox.setStyleSheet("background-color: rgb(240, 240, 240);")
#         self.original_signal_groupbox.setTitle("Original Signal")
#         sidebar_layout.addWidget(self.original_signal_groupbox)
#
#         # (3) Filtered signal groupbox
#         self.filtered_signal_groupbox = QtWidgets.QGroupBox(sidebar_layout.parent())
#         self.filtered_signal_groupbox.setStyleSheet("background-color: rgb(240, 240, 240);")
#         self.filtered_signal_groupbox.setTitle("Filtered Signal")
#         sidebar_layout.addWidget(self.filtered_signal_groupbox)
#
#         # Example: add a simple layout or a plot inside these group boxes
#         self.addGraphView(self.original_signal_groupbox)
#         self.addGraphView(self.filtered_signal_groupbox)
#
#     def setupControls(self):
#         """
#         A region for controls: checkboxes, radio buttons, slider, etc.
#         We create a horizontal layout to line them up.
#         """
#         controls_layout = self.createHorizontalLayout(self.centralwidget, 10, 399, 851, 61)
#         controls_layout.parent().setObjectName("controls_widget")
#
#         # Radio: Zeros
#         self.zeros_radioButton = QtWidgets.QRadioButton(controls_layout.parent())
#         font = QtGui.QFont()
#         font.setPointSize(11)
#         font.setBold(True)
#         self.zeros_radioButton.setFont(font)
#         self.zeros_radioButton.setText("Zeros")
#         self.zeros_radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
#         controls_layout.addWidget(self.zeros_radioButton)
#
#         # Radio: Poles
#         self.poles_radioButton = QtWidgets.QRadioButton(controls_layout.parent())
#         self.poles_radioButton.setFont(font)
#         self.poles_radioButton.setText("Poles")
#         self.poles_radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
#         controls_layout.addWidget(self.poles_radioButton)
#
#         # Checkbox: Add Conjugate
#         self.add_conjugate_checkBox = QtWidgets.QCheckBox(controls_layout.parent())
#         check_font = QtGui.QFont()
#         check_font.setPointSize(10)
#         check_font.setBold(True)
#         self.add_conjugate_checkBox.setFont(check_font)
#         self.add_conjugate_checkBox.setText("Add Conjugate")
#         self.add_conjugate_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
#         controls_layout.addWidget(self.add_conjugate_checkBox)
#
#         # Slider
#         self.horizontalSlider = self.createSlider(controls_layout, min_value=0, max_value=100, initial_value=50)
#
#         # Percentage Label
#         self.percentage = QtWidgets.QLabel(controls_layout.parent())
#         slider_label_font = QtGui.QFont()
#         slider_label_font.setFamily("Arial")
#         slider_label_font.setPointSize(15)
#         self.percentage.setFont(slider_label_font)
#         self.percentage.setStyleSheet("color: black;")
#         self.percentage.setText("50%")
#         controls_layout.addWidget(self.percentage)
#
#         # All Pass Filters Button
#         self.all_pass_filters = self.createButton(
#             controls_layout, "All Pass Filters",
#             BUTTON_STYLESHEET + "border-radius:10px;"
#         )
#
#     def setupFrequencyResponse(self):
#         """
#         Frequency response area: a horizontal layout with
#         magnitude response and phase response group boxes
#         """
#         freq_layout = self.createHorizontalLayout(self.centralwidget, 10, 460, 851, 311)
#         freq_layout.parent().setObjectName("frequency_response_widget")
#
#         # Magnitude group box
#         self.magnitude_response_groupbox = QtWidgets.QGroupBox(freq_layout.parent())
#         self.magnitude_response_groupbox.setStyleSheet("background-color: rgb(240, 240, 240);")
#         self.magnitude_response_groupbox.setTitle("Magnitude Response")
#         freq_layout.addWidget(self.magnitude_response_groupbox)
#         self.addGraphView(self.magnitude_response_groupbox)
#
#         # Phase group box
#         self.phase_response_groupbox = QtWidgets.QGroupBox(freq_layout.parent())
#         self.phase_response_groupbox.setStyleSheet("background-color: rgb(240, 240, 240);")
#         self.phase_response_groupbox.setTitle("Phase Response")
#         freq_layout.addWidget(self.phase_response_groupbox)
#         self.addGraphView(self.phase_response_groupbox)
#
#     def setupZPlane(self):
#         """
#         Z-plane area:
#          - Z-plane plot group box on the left
#          - Filter Realization group box
#          - Clear Zeros/Poles/All, Undo/Redo Buttons
#         """
#         zplane_layout = self.createHorizontalLayout(self.centralwidget, 11, 50, 849, 352)
#         zplane_layout.parent().setStyleSheet("background-color: rgb(240, 240, 240);")
#         zplane_layout.parent().setObjectName("z_plane_widget")
#
#         # Left side: Z Plane group box
#         self.z_plane_plot_groupbox = QtWidgets.QGroupBox(zplane_layout.parent())
#         self.z_plane_plot_groupbox.setTitle("Z Plane")
#         zplane_layout.addWidget(self.z_plane_plot_groupbox)
#         self.addGraphView(self.z_plane_plot_groupbox)
#
#         # Middle: Filter Realization group box
#         self.filter_realization_groupBox = QtWidgets.QGroupBox(zplane_layout.parent())
#         self.filter_realization_groupBox.setTitle("")
#         zplane_layout.addWidget(self.filter_realization_groupBox)
#         self.setupFilterRealizationControls()
#
#         # Right side: Column of buttons (Clear Zero, Clear Pole, Clear ALL, Undo, Redo)
#         button_column_layout = QtWidgets.QVBoxLayout()
#         # We can add a dummy widget to hold these buttons in a vertical line
#         dummy_widget = QtWidgets.QWidget(zplane_layout.parent())
#         dummy_widget.setLayout(button_column_layout)
#         zplane_layout.addWidget(dummy_widget)
#
#         self.clear_zeros_button = self.createButton(
#             button_column_layout, "Clear Zero",
#             """
#             QPushButton {
#                 color: #809099;
#                 background-color: rgba(255, 255, 255, 0);
#                 border: 3px solid #809099;
#                 padding: 3px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(255, 255, 255, 70);
#             }
#             """,
#             max_size=(100, 40)
#         )
#         self.clear_poles_button = self.createButton(
#             button_column_layout, "Clear Pole",
#             """
#             QPushButton {
#                 color: #809099;
#                 background-color: rgba(255, 255, 255, 0);
#                 border: 3px solid #809099;
#                 padding: 1px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(255, 255, 255, 70);
#             }
#             """,
#             max_size=(100, 40)
#         )
#         self.clear_all_button = self.createButton(
#             button_column_layout, "Clear ALL",
#             """
#             QPushButton {
#                 color: rgb(255, 255, 255);
#                 background-color: #809099;
#                 padding: 3px;
#             }
#             """,
#             max_size=(100, 40)
#         )
#         # Undo/Redo in a horizontal layout
#         undo_redo_layout = QtWidgets.QHBoxLayout()
#         self.undo_button = self.createButton(
#             undo_redo_layout, "Undo",
#             """
#             QPushButton {
#                 color: #809099;
#                 background-color: rgba(255, 255, 255, 0);
#                 border: 3px solid #809099;
#             }
#             QPushButton:hover {
#                 background-color: rgba(255, 255, 255, 10);
#             }
#             """,
#             max_size=(59, 31)
#         )
#         self.redo_button = self.createButton(
#             undo_redo_layout, "Redo",
#             """
#             QPushButton {
#                 color: #809099;
#                 background-color: rgba(255, 255, 255, 0);
#                 border: 3px solid #809099;
#             }
#             QPushButton:hover {
#                 background-color: rgba(255, 255, 255, 10);
#             }
#             """,
#             max_size=(59, 31)
#         )
#         button_column_layout.addLayout(undo_redo_layout)
#
#     def setupFilterRealizationControls(self):
#         """
#         Inside self.filter_realization_groupBox, put 'Structure' & 'Code' buttons,
#         plus the built-in library combo box, etc.
#         """
#         flayout = QtWidgets.QHBoxLayout(self.filter_realization_groupBox)
#         # Buttons
#         self.filter_realizaion_structure = QtWidgets.QPushButton("Structure", self.filter_realization_groupBox)
#         self.filter_realizaion_structure.setStyleSheet("""
#             QPushButton {
#                 color: rgb(0, 0, 0);
#                 background-color: rgba(255, 255, 255, 0);
#                 border: 2px solid #809099;
#                 padding: 1px;
#                 border-radius: 7px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(255, 255, 255, 70);
#             }
#         """)
#         self.filter_realizaion_structure.setFixedWidth(80)
#         flayout.addWidget(self.filter_realizaion_structure)
#
#         self.filter_realizaion_code = QtWidgets.QPushButton("Code", self.filter_realization_groupBox)
#         self.filter_realizaion_code.setStyleSheet("""
#             QPushButton {
#                 color: rgb(0, 0, 0);
#                 background-color: rgba(255, 255, 255, 0);
#                 border: 2px solid #809099;
#                 padding: 1px;
#                 border-radius: 7px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(255, 255, 255, 70);
#             }
#         """)
#         self.filter_realizaion_code.setFixedWidth(80)
#         flayout.addWidget(self.filter_realizaion_code)
#
#         # Built-in library combo
#         self.built_In_library_comboBox = QtWidgets.QComboBox(self.filter_realization_groupBox)
#         self.built_In_library_comboBox.setStyleSheet("""
#             QComboBox {
#                 color: rgb(0, 0, 0);
#                 background-color: rgba(255, 255, 255, 0);
#                 border: 2px solid #809099;
#                 padding: 1px;
#                 border-radius: 7px;
#             }
#         """)
#         self.built_In_library_comboBox.addItems(["Library1", "Library2"])
#         flayout.addWidget(self.built_In_library_comboBox)
#
#     # -----------------------------------------------------------
#     # Example: embedding a PlotWidget in a group box
#     # -----------------------------------------------------------
#     def addGraphView(self, group_box):
#         """
#         Example method to add a pyqtgraph PlotWidget into a QGroupBox
#         using a layout.
#         """
#         plot_widget = pg.PlotWidget()
#         plot_widget.setBackground((240, 240, 240, 0.5))
#         plot_widget.showGrid(x=True, y=True, alpha=0.5)
#
#         box_layout = QtWidgets.QVBoxLayout(group_box)
#         box_layout.addWidget(plot_widget)
#         group_box.setLayout(box_layout)
#
#         return plot_widget
#
#     # -----------------------------------------------------------
#     # For retranslation
#     # -----------------------------------------------------------
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         # If you need specific text changes, do them here.
#         # e.g.: self.app_title.setText(_translate("MainWindow", "Digital Filter"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
