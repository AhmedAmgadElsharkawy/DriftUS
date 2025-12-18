from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDoubleSpinBox, QLabel

class SpinBox(QWidget):
    def __init__(self, label_text="Select Value:", initial_value=0,step = 0.1, decimals = 1, start = -100, end = 100):
        super().__init__()
        central_layout = QVBoxLayout(self)
        central_layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        
        self.spin_box = QDoubleSpinBox()
        
        self.spin_box.setRange(start, end)  
        self.spin_box.setSingleStep(step)     
        self.spin_box.setDecimals(decimals)         
        self.spin_box.setValue(initial_value) 
        
        central_layout.addWidget(self.label)
        central_layout.addWidget(self.spin_box)



    def value(self):
        return round(self.spin_box.value(), self.spin_box.decimals())
    
    def set_font(self, font):
        self.label.setFont(font)
        self.spin_box.setFont(font)