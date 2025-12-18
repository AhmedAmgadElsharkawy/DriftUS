from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt

class ListItem(QWidget):
    def __init__(self, item_obj, index, delete_callback = None):
        super().__init__()
        self.item = item_obj
        self.delete_callback = delete_callback
        self.index = index

        
        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Normal) 

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        self.label = QLabel(item_obj.name)
        self.label.setFont(font)
        layout.addWidget(self.label)

        if(delete_callback):
            self.delete_button = QToolButton()
            self.delete_button.setObjectName("item_delete_button")
            self.delete_button.setIcon(QIcon("assets/icons/trash.svg"))
            self.delete_button.setIconSize(QSize(24, 24))
            self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.delete_button.clicked.connect(lambda: self.delete_callback(self.index))
            layout.addWidget(self.delete_button)
