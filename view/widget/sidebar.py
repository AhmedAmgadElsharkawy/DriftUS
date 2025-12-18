from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidgetItem,
    QLabel, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, Qt


from view.widget.scrollable_list import ScrollableList
from view.widget.spin_box import SpinBox
from model.point_item import PointItem

class Sidebar(QWidget):
    currentIndexChanged = pyqtSignal(int)
    point_added = pyqtSignal(float, float)
    loadPhantomRequested = pyqtSignal()

    def __init__(self,main_window):
        super().__init__()
        self.setFixedWidth(330)

        self.roi_enabled = False
        self.line_enabled = False

        self.main_window = main_window

        self.centeral_layout = QVBoxLayout(self)
        self.centeral_layout.setContentsMargins(0, 0, 0, 0)
        self.centeral_layout.setSpacing(0)

        self.main_widget = QWidget()
        self.main_widget.setObjectName("sidebar_main_widget")
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.main_widget_layout.setSpacing(0)
        self.centeral_layout.addWidget(self.main_widget)

        self.controls_container = QWidget()
        self.controls_container_layout = QVBoxLayout(self.controls_container)
        self.controls_container_layout.setContentsMargins(16, 16, 16, 16)
        self.controls_container_layout.setSpacing(24)
        self.main_widget_layout.addWidget(self.controls_container)

        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Normal) 

        self.speed_spin_box = SpinBox(label_text="Speed")
        self.speed_spin_box.set_font(font)
        self.controls_container_layout.addWidget(self.speed_spin_box)

        self.add_point_container = QWidget()
        self.add_point_container.setObjectName("sidebar_buttons_container")
        self.add_point_container_layout = QVBoxLayout(self.add_point_container)
        self.add_point_container_layout.setContentsMargins(0,0,0,0)
        self.add_point_container_layout.setSpacing(8)
        self.controls_container_layout.addWidget(self.add_point_container)

        self.add_point_inputs_container = QWidget()
        self.add_point_inputs_container_layout = QHBoxLayout(self.add_point_inputs_container)
        self.add_point_inputs_container_layout.setContentsMargins(0,0,0,0)
        self.add_point_inputs_container_layout.setSpacing(8)
        self.add_point_container_layout.addWidget(self.add_point_inputs_container)

        self.depth_spin_box = SpinBox(label_text="Depth")
        self.lateral_spin_box = SpinBox(label_text="Lateral")
        self.depth_spin_box.set_font(font)
        self.lateral_spin_box.set_font(font)
        self.add_point_inputs_container_layout.addWidget(self.depth_spin_box)
        self.add_point_inputs_container_layout.addWidget(self.lateral_spin_box)

        self.add_point_button = QPushButton("Add Point")
        self.add_point_button.setCursor(Qt.CursorShape.PointingHandCursor)
        font.setWeight(QFont.Weight.Medium) 
        self.add_point_button.setFont(font)
        self.add_point_button.setObjectName("add_point_button")
        self.add_point_container_layout.addWidget(self.add_point_button)
        self.add_point_button.clicked.connect(self.on_point_added)

        self.item_list_container = QWidget()
        self.item_list_container.setObjectName("item_list_container")
        self.item_list_container_layout = QVBoxLayout(self.item_list_container)
        self.item_list_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.item_list_container_layout.setContentsMargins(16,16,0,0)
        self.item_list_container_layout.setSpacing(0)
        self.main_widget_layout.addWidget(self.item_list_container)

        font = QFont("Segoe UI", 12)
        font.setWeight(QFont.Weight.Medium) 

        self.item_list_header = QLabel("Points")
        self.item_list_header.setFont(font)
        self.item_list_container_layout.addWidget(self.item_list_header)
        self.item_list_header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.item_list = ScrollableList()
        self.item_list_container_layout.addWidget(self.item_list, stretch=1)


    def on_point_added(self):
        new_point = PointItem(
            depth= self.depth_spin_box.value(),
            lateral= self.lateral_spin_box.value()
        )
        
        self.item_list.append_item(new_point)

                
