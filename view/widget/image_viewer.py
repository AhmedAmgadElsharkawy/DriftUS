import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QColor, QFont

class ImageViewer(QWidget):
    def __init__(self, main_window, header = "Viewer"):
        super().__init__()

        self.main_window = main_window

        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        self.main_widget = QWidget()
        self.main_widget.setObjectName("image_viewer_main_widget")
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(16,16,16,16)
        self.main_widget_layout.setSpacing(24)
        self.central_layout.addWidget(self.main_widget)

        self.header_container = QWidget()
        self.header_container_layout = QHBoxLayout(self.header_container)
        self.header_container_layout.setContentsMargins(0,0,0,0)
        self.main_widget_layout.addWidget(self.header_container)
    
        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Normal) 

        self.viewer_label = QLabel(header)
        self.viewer_label.setFont(font)
        self.header_container_layout.addWidget(self.viewer_label )

        self.image_view = pg.ImageView()
        self.image_view.getView().setBackgroundColor(QColor("#edf2f8"))
        self.image_view.ui.histogram.hide()
        self.image_view.ui.roiBtn.hide()
        self.image_view.ui.menuBtn.hide()
        self.main_widget_layout.addWidget(self.image_view)

        self.image_view.getView().invertY(False)
        self.image_view.getView().setAspectLocked(True)

        self.data = None

    def set_image(self, data: np.ndarray):
        self.data = data
        self.image_view.setImage(data.T, autoLevels=True)

    









