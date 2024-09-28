import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSlider, QGraphicsView, QGraphicsScene,
                             QGraphicsRectItem, QGraphicsPixmapItem, QDialog, QTextBrowser,
                             QLineEdit)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QImage, QPixmap, QWheelEvent, QMouseEvent, QPen, QColor, QPainter, QIntValidator


from ._view import GEGraphicsView
from ._dialog import CellDataDialog

from ._window import GridEngineUI


if 'ui' in sys.argv:
    app = QApplication(sys.argv)
    window = GridEngineUI()
    window.show()
    sys.exit(app.exec_())