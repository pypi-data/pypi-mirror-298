from . import *

class GEGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(1, 1)
        self.zoom_factor = 1.15
        self.zoom_level = 0
        self.max_zoom_level = 10
        self.min_zoom_level = -10

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_factor
            self.zoom_level += 1
        else:
            zoom_factor = 1 / self.zoom_factor
            self.zoom_level -= 1

        if self.min_zoom_level <= self.zoom_level <= self.max_zoom_level:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.zoom_level = max(min(self.zoom_level, self.max_zoom_level), self.min_zoom_level)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
        super().mouseReleaseEvent(event)