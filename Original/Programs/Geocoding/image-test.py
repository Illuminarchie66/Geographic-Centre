import requests
import keyboard
import urllib
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

with open('API-KEY.txt') as f:
    api_key = f.readline()
    f.close()


urllib.request.urlretrieve("http://maps.googleapis.com/maps/api/staticmap?center=-0.0,0.0&size=600x600&key="+api_key+"&sensor=false", "map1.jpg")
urllib.request.urlretrieve("http://maps.googleapis.com/maps/api/staticmap?center=-0.0,0.0&size=600x600&key="+api_key+"&zoom=3&sensor=false", "00000002.jpg")


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1500
        self.height = 900
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('map1.jpg')
        label.setPixmap(pixmap)
        label.move(500, 0)

        self.line_edit1 = QLineEdit(self)
        self.line_edit1.move(20, 50)
        self.line_edit1.returnPressed.connect(self.on_line_edit1_returnPressed)

        self.show()

    def on_line_edit1_returnPressed(self):
        print(self.line_edit1.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())