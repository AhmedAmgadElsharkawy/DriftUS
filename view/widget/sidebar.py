from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QLabel, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal


from view.widget.scrollable_list import ScrollableList
from view.widget.spin_box import SpinBox

from model.cyst_item import CystItem

from utils.toast_utils import show_toast

class Sidebar(QWidget):
    speed_changed = pyqtSignal(float)

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
        self.speed_spin_box.value_changed.connect(self.on_speed_changed)
        self.speed_spin_box.set_font(font)
        self.controls_container_layout.addWidget(self.speed_spin_box)

        self.add_cyst_container = QWidget()
        self.add_cyst_container.setObjectName("sidebar_buttons_container")
        self.add_cyst_container_layout = QVBoxLayout(self.add_cyst_container)
        self.add_cyst_container_layout.setContentsMargins(0,0,0,0)
        self.add_cyst_container_layout.setSpacing(8)
        self.controls_container_layout.addWidget(self.add_cyst_container)

        self.add_cyst_inputs_container = QWidget()
        self.add_cyst_inputs_container_layout = QHBoxLayout(self.add_cyst_inputs_container)
        self.add_cyst_inputs_container_layout.setContentsMargins(0,0,0,0)
        self.add_cyst_inputs_container_layout.setSpacing(8)
        self.add_cyst_container_layout.addWidget(self.add_cyst_inputs_container)

        self.depth_spin_box = SpinBox(label_text="Depth", decimals=3, initial_value=0.025)
        self.lateral_spin_box = SpinBox(label_text="Lateral", decimals=3, initial_value=-0.010)
        self.radius_spin_box = SpinBox(label_text="Radius", decimals=3, initial_value=0.004)
        self.depth_spin_box.set_font(font)
        self.lateral_spin_box.set_font(font)
        self.radius_spin_box.set_font(font)
        self.add_cyst_inputs_container_layout.addWidget(self.depth_spin_box)
        self.add_cyst_inputs_container_layout.addWidget(self.lateral_spin_box)
        self.add_cyst_inputs_container_layout.addWidget(self.radius_spin_box)

        self.add_cyst_button = QPushButton("Add Cyst")
        self.add_cyst_button.setCursor(Qt.CursorShape.PointingHandCursor)
        font.setWeight(QFont.Weight.Medium) 
        self.add_cyst_button.setFont(font)
        self.add_cyst_button.setObjectName("add_cyst_button")
        self.add_cyst_container_layout.addWidget(self.add_cyst_button)
        self.add_cyst_button.clicked.connect(self.on_cyst_added)

        self.item_list_container = QWidget()
        self.item_list_container.setObjectName("item_list_container")
        self.item_list_container_layout = QVBoxLayout(self.item_list_container)
        self.item_list_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.item_list_container_layout.setContentsMargins(16,16,0,0)
        self.item_list_container_layout.setSpacing(0)
        self.main_widget_layout.addWidget(self.item_list_container)

        font = QFont("Segoe UI", 12)
        font.setWeight(QFont.Weight.Medium) 

        self.item_list_header = QLabel("Cysts")
        self.item_list_header.setFont(font)
        self.item_list_container_layout.addWidget(self.item_list_header)
        self.item_list_header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.item_list = ScrollableList(self.main_window)
        self.item_list_container_layout.addWidget(self.item_list, stretch=1)


    def on_cyst_added(self):
        new_cyst = CystItem(
            depth= self.depth_spin_box.value(),
            lateral= self.lateral_spin_box.value(),
            radius = self.radius_spin_box.value()
        )
        
        is_cyst_exists = self.main_window.phantom_controller.is_cyst_exists(new_cyst)

        if is_cyst_exists:
            show_toast(self.main_window, "Cyst Already Exists",f"Cyst (d={self.depth_spin_box.value()}, l={self.lateral_spin_box.value()}, r={self.radius_spin_box.value()}) already exists.")
            return
        
        self.main_window.phantom_controller.add_cyst(new_cyst)
        self.item_list.append_item(new_cyst)

        show_toast(self.main_window, "Cyst Added",f"Cyst (d={self.depth_spin_box.value()}, l={self.lateral_spin_box.value()}, r={self.radius_spin_box.value()}) added successfully.")


    def on_speed_changed(self, speed):
        self.speed_changed.emit(speed)

                
