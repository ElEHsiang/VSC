from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MyQLabel(QLabel):
    """Clickable QLabel
    
    Signal:
        click_pos: sent mouse position when press        
    """
    click_pos = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        self.click_pos.emit(event.x(), event.y())

