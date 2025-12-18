import os
from PyQt5.QtCore import QFile, QTextStream

def load_stylesheet(theme="light"):
    base_path = os.path.dirname(__file__)
    qss_path = os.path.join(base_path, "..", "assets", "styles", f"{theme}.qss")
    qss_path = os.path.abspath(qss_path)

    file = QFile(qss_path)
    if not file.open(QFile.ReadOnly | QFile.Text):
        print(f"Could not load stylesheet: {qss_path}")
        return ""

    stream = QTextStream(file)
    return stream.readAll()


def apply_stylesheet(widget, theme="light"):
    qss = load_stylesheet(theme)
    widget.setStyleSheet(qss)