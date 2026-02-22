import urllib
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 500
        self.top = 200
        self.width = 800
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 50)
        self.textbox.returnPressed.connect(self.on_textbox_returnPressed)

        self.show()

    def on_textbox_returnPressed(self):
        print(self.textbox.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


#label = QLabel(self)
        #pixmap = QPixmap('map1.jpg')
        #label.setPixmap(pixmap)
        #label.move(500, 0)