from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import mkBrush, mkColor
from PyQt5.QtWidgets import QComboBox

# Global Colors and Styles
MAIN_BACKGROUND_COLOR = """
    background-color: rgb(128, 144, 153);
"""
WIDGET_BORDER_STYLE = """
    border: 1px solid #fff;
"""
BUTTON_STYLE = """
    QPushButton {
        color: #fff;
        background-color: none;
        border: 3px solid #fff;
        padding: 8px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 25);
    }
"""
Z_BUTTON_STYLE = """
    QPushButton {
        color:#373B36;
        background-color: none;
        border: 3px solid #373B36;
        padding: 2px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 25);
    }
"""
GROUPBOX_STYLE = """
    background-color: #F0F0F0;
    color: black;
"""
LABEL_STYLE = """
    color: rgb(255, 255, 255);
"""
SLIDER_STYLE = """
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
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setStyleSheet(MAIN_BACKGROUND_COLOR)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Setup individual components
        self.setup_main(MainWindow)
        self.setup_sidebar()
        self.setup_layout_widget()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_main(self, MainWindow):
        # Main header widget
        self.header_widget = QtWidgets.QWidget(self.centralwidget)
        self.header_widget.setGeometry(QtCore.QRect(10, 0, 1261, 48))
        self.header_widget.setStyleSheet(WIDGET_BORDER_STYLE)

        # App Title
        self.app_title = self.create_label(self.header_widget, 0, 0, 221, 47, "Digital Filter", 29, "Arial")

        # Buttons in header
        self.save_filter_button = self.create_button(self.header_widget, 410, 7, 125, 37, "Save Filter")
        self.load_filter_button = self.create_button(self.header_widget, 260, 7, 125, 37, "Load Filter")
        # Replace the button creation with a QComboBox
        self.filters_library_combobox = QComboBox(self.header_widget)
        self.filters_library_combobox.setGeometry(590, 7, 181, 37)  # Set position and size
        self.quit_button = self.create_button(self.header_widget, 1130, 7, 125, 37, "Quit App")
        self.quit_button.clicked.connect(QtWidgets.QApplication.quit)

    def setup_sidebar(self):
        # Sidebar layout
        self.sidebar_widget = QtWidgets.QWidget(self.centralwidget)
        self.sidebar_widget.setGeometry(QtCore.QRect(870, 60, 405, 700))
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(20)

        # Mouse controller
        self.mouse_controller_layout = QtWidgets.QVBoxLayout()
        self.label = self.create_label(self.sidebar_widget, 0, 0, 285, 20, "Move your mouse here to generate signal", 11, "Arial")
        self.mouse_controller_layout.addWidget(self.label)

        self.padding_area = QtWidgets.QWidget(self.sidebar_widget)
        self.padding_area.setStyleSheet(GROUPBOX_STYLE + "border-radius: 10px;")
        self.padding_area.setMinimumSize(200, 200)
        self.mouse_controller_layout.addWidget(self.padding_area)
        self.sidebar_layout.addLayout(self.mouse_controller_layout)

        # Add group boxes
        self.original_signal_groupbox = self.create_groupbox("Original Signal", self.sidebar_widget)
        self.original_plot_widget = self.addGraphView(self.original_signal_groupbox)

        self.filtered_signal_groupbox = self.create_groupbox("Filtered Signal", self.sidebar_widget)
        self.filtered_plot_widget = self.addGraphView(self.filtered_signal_groupbox)

        self.sidebar_layout.addWidget(self.original_signal_groupbox)
        self.sidebar_layout.addWidget(self.filtered_signal_groupbox)

    def setup_layout_widget(self):
        # Main layout widget
        self.layout_widget = QtWidgets.QWidget(self.centralwidget)
        self.layout_widget.setGeometry(QtCore.QRect(10, 50, 851, 711))
        self.layout_widget.setObjectName("layoutWidget")
        self.main_layout = QtWidgets.QVBoxLayout(self.layout_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Z Plane widget
        self.z_plane_widget = QtWidgets.QWidget(self.layout_widget)
        self.z_plane_widget.setStyleSheet(GROUPBOX_STYLE)
        self.main_layout.addWidget(self.z_plane_widget)

        # Z Plane plot group box
        self.z_plane_plot_groupbox = self.create_groupbox("Z Plane", self.z_plane_widget, 0, 0, 400, 400)
        self.z_plane_plot_widget = self.addGraphView(self.z_plane_plot_groupbox)
        # self.z_plane_plot_widget.showGrid(x=False, y=False)

        # Sliders and buttons
        self.horizontalSlider = QtWidgets.QSlider(self.z_plane_widget)
        self.horizontalSlider.setGeometry(QtCore.QRect(470, 250, 300, 21))
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setStyleSheet(SLIDER_STYLE)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(50)

        self.slider_label = self.create_label(self.z_plane_widget, 780, 245, 40, 30, "50%", 15, "Arial", "color: black;")

        self.clear_zeros_button = self.create_button(self.z_plane_widget, 710, 60, 125, 40, "Clear Zeros", True)
        self.clear_all_button = self.create_button(self.z_plane_widget, 710, 300, 125, 40, "Clear ALL", True)
        self.clear_poles_button = self.create_button(self.z_plane_widget, 710, 110, 125, 40, "Clear Poles", True)
        self.swap_button = self.create_button(self.z_plane_widget, 710, 160, 125, 40, "Swap", True)
        self.undo_button = self.create_button(self.z_plane_widget, 530, 310, 71, 31, "Undo", True)
        self.redo_button = self.create_button(self.z_plane_widget, 450, 310, 71, 31, "Redo", True)

        # Add radio buttons and checkbox
        self.add_conjugate_checkBox = QtWidgets.QCheckBox(self.z_plane_widget)
        self.add_conjugate_checkBox.setGeometry(QtCore.QRect(450, 70, 160, 23))
        font = QtGui.QFont("", 10, QtGui.QFont.Bold)
        self.add_conjugate_checkBox.setFont(font)
        self.add_conjugate_checkBox.setText("Add Conjugate")

        self.poles_radioButton = QtWidgets.QRadioButton(self.z_plane_widget)
        self.poles_radioButton.setGeometry(QtCore.QRect(450, 170, 88, 19))
        self.poles_radioButton.setFont(font)
        self.poles_radioButton.setText("Poles")

        self.zeros_radioButton = QtWidgets.QRadioButton(self.z_plane_widget)
        self.zeros_radioButton.setGeometry(QtCore.QRect(450, 140, 88, 19))
        self.zeros_radioButton.setFont(font)
        self.zeros_radioButton.setText("Zeros")

        # Frequency response layout
        self.frequency_response_layout = QtWidgets.QHBoxLayout()
        self.magnitude_response_groupbox = self.create_groupbox("Magnitude Response", self.layout_widget)
        self.magnitude_plot_widget = self.addGraphView(self.magnitude_response_groupbox)

        self.phase_response_groupbox = self.create_groupbox("Phase Response", self.layout_widget)
        self.phase_plot_widget = self.addGraphView(self.phase_response_groupbox)

        self.frequency_response_layout.addWidget(self.magnitude_response_groupbox)
        self.frequency_response_layout.addWidget(self.phase_response_groupbox)
        self.main_layout.addLayout(self.frequency_response_layout)

    def create_button(self, parent, x, y, width, height, text, inZplane=False):
        button = QtWidgets.QPushButton(parent)
        button.setGeometry(QtCore.QRect(x, y, width, height))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        button.setFont(font)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button_stylesheet = Z_BUTTON_STYLE if inZplane else BUTTON_STYLE
        button.setStyleSheet(button_stylesheet)
        button.setText(text)
        return button

    def create_groupbox(self, title, parent, x=0, y=0, width=400, height=150):
        groupbox = QtWidgets.QGroupBox(parent)
        groupbox.setGeometry(QtCore.QRect(x, y, width, height))
        groupbox.setStyleSheet(GROUPBOX_STYLE)
        groupbox.setTitle(title)
        return groupbox

    def create_label(self, parent, x, y, width, height, text, font_size, font_family, style=LABEL_STYLE):
        label = QtWidgets.QLabel(parent)
        label.setGeometry(QtCore.QRect(x, y, width, height))
        font = QtGui.QFont(font_family, font_size)
        label.setFont(font)
        label.setStyleSheet(style)
        label.setText(text)
        return label

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

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Digital Filter")

    def update_slider_label(self):
        self.slider_label.setText(f"{self.horizontalSlider.value()}%")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
