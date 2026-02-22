import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MapApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title='Big-test'
        self.left=0
        self.top=0
        self.width=1202
        self.height=850
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)

        self.line_edit1 = QLineEdit(self)
        self.line_edit1.move(50, 50)
        self.line_edit1.returnPressed.connect(self.on_line_edit1_returnPressed)

        label = QLabel(self)
        pixmap = QPixmap('Fischl.jpg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()

    #def on_line_edit1_returnPressed(self):
        #print(self.line_edit1.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApp()
    sys.exit(app.exec_())
