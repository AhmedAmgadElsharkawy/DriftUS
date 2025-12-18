from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from view.widget.metric_widget import MetricWidget
from view.widget.sidebar import Sidebar 
from view.widget.image_viewer import ImageViewer

from view.style_manager import apply_stylesheet

class MainWindow(QMainWindow):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            return super(MainWindow, cls).__new__(cls)
        return cls.__instance     

    def __init__(self):
        if MainWindow.__instance is not None:
            return
        
        super().__init__() 
        MainWindow.__instance = self

        self.setWindowTitle("DriftUS")


        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("main_widget")
        self.main_widget.setObjectName("main_widget")
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QHBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        self.main_widget_layout.addWidget(self.sidebar)

        self.body_container = QWidget()
        self.body_container_layout = QVBoxLayout(self.body_container)
        self.body_container_layout.setContentsMargins(24, 24, 24, 24)
        self.body_container_layout.setSpacing(16)
        self.main_widget_layout.addWidget(self.body_container)


        self.image_viewers_container = QWidget()
        self.image_viewers_container_layout = QHBoxLayout(self.image_viewers_container)
        self.image_viewers_container_layout.setContentsMargins(0,0,0,0)
        self.image_viewers_container_layout.setSpacing(24)
        self.body_container_layout.addWidget(self.image_viewers_container, stretch=1)

        self.phantom_image_viewer = ImageViewer(self, header= "Phantom")
        self.reconstructed_image_viewer = ImageViewer(self, header = "Reconstructed Image")
        self.image_viewers_container_layout.addWidget(self.phantom_image_viewer)
        self.image_viewers_container_layout.addWidget(self.reconstructed_image_viewer)

        
        self.quantitative_metrics_container = QWidget()
        self.quantitative_metrics_container_layout = QHBoxLayout(self.quantitative_metrics_container)
        self.quantitative_metrics_container.setObjectName("quantitative_metrics_container")
        self.quantitative_metrics_container_layout.setContentsMargins(16,16,16,16)
        self.quantitative_metrics_container_layout.setSpacing(0)

        self.m1 = MetricWidget("Metric 1")
        self.quantitative_metrics_container_layout.addWidget(self.m1)
        self.m2 = MetricWidget("Metric 2")
        self.quantitative_metrics_container_layout.addWidget(self.m2)
        self.m3 = MetricWidget("Metric 3")
        self.quantitative_metrics_container_layout.addWidget(self.m3)
        self.m4 = MetricWidget("Metric 4")
        self.quantitative_metrics_container_layout.addWidget(self.m4)


        self.body_container_layout.addWidget(self.quantitative_metrics_container, stretch=0)


        # add controllers here
        


        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.showMaximized()

        apply_stylesheet(self, "light")
