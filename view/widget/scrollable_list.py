from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem, QLabel, QSizePolicy
)

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from view.widget.list_item import ListItem

from utils.toast_utils import show_toast

class ScrollableList(QWidget):   
    items_list_updated = pyqtSignal(list)
 
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.items = []
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(0)

        self.main_widget = QWidget()
        self.central_layout.addWidget(self.main_widget)
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.main_widget_layout.setSpacing(0)
        self.main_widget_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) 

        font = QFont("Segoe UI", 12)
        font.setWeight(QFont.Weight.Light) 
        self.no_items_label = QLabel("No cysts added")
        self.no_items_label.setFont(font)
        self.main_widget_layout.addWidget(self.no_items_label)
        self.no_items_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.items_list = QListWidget()
        self.items_list.setFocusPolicy(Qt.NoFocus)
        self.items_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.items_list.setObjectName("item_list")
        self.main_widget_layout.addWidget(self.items_list, stretch=1)
        self.items_list.setVisible(False)


    def update_item_list(self):
        self.items_list.clear()
        if len(self.items) > 0:
            self.no_items_label.setVisible(False)
            self.items_list.setVisible(True)
        else:
            self.no_items_label.setVisible(True)
            self.items_list.setVisible(False)

        for i, s in enumerate(self.items):
            delete_callback = self.delete_item
            item_widget = ListItem(item_obj=s, delete_callback=delete_callback, index=i)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.items_list.addItem(item)
            self.items_list.setItemWidget(item, item_widget)

        self.items_list_updated.emit(self.items)


    def delete_item(self, index):
        if 0 <= index < len(self.items):
            show_toast(self.main_window, "Cyst Deleted", f"Cyst (d={self.items[index].get_depth()}, l={self.items[index].get_lateral()}, r={self.items[index].get_radius()}) deleted successfully.")
            del self.items[index]
            for i, s in enumerate(self.items):
                s.index = i
            self.update_item_list()

    def append_item(self,new_item):
        self.items.append(new_item)
        self.update_item_list()

    def set_items(self,new_items):
        self.items = new_items
        self.update_item_list()

    def itemWidget(self, item):
        return self.items_list.itemWidget(item)

    def get_items(self):
        return self.items


