import sys
from PyQt5.QtWidgets import QApplication
from view.window.main_window import MainWindow
from PyQt5.QtGui import QIcon

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icons/favicon.png"))
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()