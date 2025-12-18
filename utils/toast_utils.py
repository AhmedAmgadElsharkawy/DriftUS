from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from pyqttoast import Toast as PyQtToast, ToastPreset

def show_toast(parent, title="Success!", text="Finished", type="SUCCESS"):
    toast = PyQtToast(parent)
    toast.setPositionRelativeToWidget(parent)
    toast.setFixedSize(QSize(350, 80))
    toast.setDuration(3000)
    toast.setTitle(title)
    toast.setText(text)

    if type == "SUCCESS":
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.setIconColor(QColor('#0071df'))
        toast.setDurationBarColor(QColor('#0071df'))
    elif type == "ERROR":
        toast.applyPreset(ToastPreset.ERROR)
        toast.setIconColor(QColor('#FF5F56'))
        toast.setDurationBarColor(QColor('#FF5F56'))
    else:
        print("Wrong Toast Type")

    toast.show()
