from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MetricWidget(QWidget):
    def __init__(self, name: str, initial_value="N/A"):
        super().__init__()

        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Normal) 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.label = QLabel(name+":")
        self.value_label = QLabel(initial_value)
        font = QFont("Segoe UI", 9)
        font.setWeight(QFont.Weight.Light) 
        self.label.setFont(font)
        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Normal) 
        self.value_label.setFont(font)
        self.value_label.setObjectName("metric_value_label")

        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.label)
        layout.addWidget(self.value_label)

    def set_value(self, value):
        self.value_label.setText(str(value))
