from PyQt6 import QtWidgets
import sys

class UI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("每日一語")
        self.resize(320, 240)
        self.setStyleSheet("background:#fcc;")
        self.main_page()
    
    def main_page(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("hello world")
        self.label.move(50,50)
        self.label.setStyleSheet("font-size:30px; color:#00c")

if __name__ == "__main__":
    main = QtWidgets.QApplication(sys.argv)
    UI = UI()
    UI.show()
    sys.exit(main.exec())