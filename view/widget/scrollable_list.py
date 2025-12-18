from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem, QLabel, QSizePolicy
)

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from view.widget.list_item import ListItem

class ScrollableList(QWidget):
    itemSelectionChanged = pyqtSignal()
    
    def __init__(self, selectable=False, multi_select=False, delete = True):
        super().__init__()

        self.items = []
        self.delete = delete
        self.selectable = selectable
        self.multi_select = multi_select

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
        self.no_items_label = QLabel("No points added")
        self.no_items_label.setFont(font)
        self.main_widget_layout.addWidget(self.no_items_label)
        self.no_items_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.items_list = QListWidget()
        self.items_list.setFocusPolicy(Qt.NoFocus)
        self.items_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.items_list.setObjectName("item_list")
        self.main_widget_layout.addWidget(self.items_list, stretch=1)
        self.items_list.setVisible(False)

        if self.selectable:
            self.items_list.setSelectionMode(
                QAbstractItemView.MultiSelection if self.multi_select else QAbstractItemView.SingleSelection
            )
        else:
            self.items_list.setSelectionMode(QAbstractItemView.NoSelection)

        self.items_list.itemSelectionChanged.connect(self.itemSelectionChanged.emit)



    def update_item_list(self):
        self.items_list.clear()
        if len(self.items) > 0:
            self.no_items_label.setVisible(False)
            self.items_list.setVisible(True)

        for i, s in enumerate(self.items):
            delete_callback = self.delete_item if self.delete else None
            item_widget = ListItem(item_obj=s, delete_callback=delete_callback, index=i)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.items_list.addItem(item)
            self.items_list.setItemWidget(item, item_widget)

    def delete_item(self, index):
        if 0 <= index < len(self.items):
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


    def selectedItems(self):
        return self.items_list.selectedItems()

    def itemWidget(self, item):
        return self.items_list.itemWidget(item)

    def clearSelection(self):
        self.items_list.clearSelection()

    def setSelectionMode(self, mode):
        self.items_list.setSelectionMode(mode)

    def get_selected_items(self):
        return [
            self.itemWidget(item).item_obj
            for item in self.selectedItems()
            if self.itemWidget(item) is not None
        ]


