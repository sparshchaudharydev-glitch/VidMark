from PyQt5.QtWidgets import QSlider, QToolTip
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtGui import QPainter, QColor

class BookmarkSeeker(QSlider):
 
    bookmark_clicked = pyqtSignal(int,str)

    def __init__(self):
        self.marker_color = QColor("orange")
        super().__init__(Qt.Horizontal)
        self.bookmark = []
        self.setMouseTracking(True)

    def set_bookmark(self,bookmarks):
        self.bookmark = bookmarks
        self.update()

    def paintEvent(self, ev):
        super().paintEvent(ev)

        painter = QPainter(self)
        
        painter.setBrush(self.marker_color)
        for i in self.bookmark:
            x = int(i.timestamp/self.maximum()*self.width())
            painter.drawRect(x,0,20,20)
        painter.end()

    def mousePressEvent(self, ev):
        click = ev.x()
        for i in self.bookmark:
            each_book = int(i.timestamp/self.maximum()*self.width())
            if abs(each_book - click) < 6 :
                self.seekto = i.timestamp
        super().mousePressEvent(ev) 
        
    def mouseMoveEvent(self, ev):
        hover = ev.x()
        for i in self.bookmark:
            each_book = int(i.timestamp/self.maximum()*self.width())
            if abs(each_book - hover) < 6 :
                QToolTip.showText(self.mapToGlobal(ev.pos()), i.label)
        super().mouseMoveEvent(ev) 
        
    def set_marker_color(self,color):
        self.marker_color = QColor(color)
        self.update()
    
    

    
        

        
        
    