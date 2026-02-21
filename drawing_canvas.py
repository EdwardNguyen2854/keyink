"""Drawing canvas overlay for annotations."""

from PySide6.QtCore import Qt, QPoint, QPointF, QTimer, QRectF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath, QPixmap, QScreen, QRegion
from PySide6.QtWidgets import QWidget

DRAWING_TOOL_PEN = "pen"
DRAWING_TOOL_RECT = "rect"
DRAWING_TOOL_ELLIPSE = "ellipse"
DRAWING_TOOL_ARROW = "arrow"
DRAWING_TOOL_LINE = "line"


class DrawingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowDoesNotAcceptFocus
        )
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)

        self._shapes = []
        self._current_shape = None
        self._tool = DRAWING_TOOL_PEN
        self._color = QColor("#FF4444")
        self._stroke_width = 4
        self._opacity = 15  # Default opacity (0-255)
        self._is_drawing = False
        self._start_point = QPoint()
        self._cursor_pos = QPoint()
        self._main_window = None
        self._mask_timer = QTimer(self)
        self._mask_timer.timeout.connect(self._update_mask)
        self._mask_timer.setInterval(100)

        self._update_geometry()

    def set_main_window(self, window):
        self._main_window = window

    def _update_geometry(self):
        screen = self.screen()
        if screen:
            self.setGeometry(screen.geometry())
            self.setFixedSize(screen.size())
        self._update_mask()

    def _update_mask(self):
        if not self._main_window:
            return
        if not self._main_window.isVisible():
            return
        if self._is_drawing:
            return
        screen_geo = self.geometry()
        app_geo = self._main_window.geometry()
        app_rect = QRegion(
            app_geo.x(), app_geo.y(),
            app_geo.width(), app_geo.height()
        )
        full_screen = QRegion(screen_geo.x(), screen_geo.y(), screen_geo.width(), screen_geo.height())
        masked = full_screen.subtracted(app_rect)
        self.setMask(masked)

    def showEvent(self, event):
        super().showEvent(event)
        self._update_geometry()
        self._mask_timer.start()

    def hideEvent(self, event):
        self._mask_timer.stop()
        super().hideEvent(event)

    def screenChanged(self, screen):
        self._update_geometry()

    def set_tool(self, tool: str):
        self._tool = tool

    def set_color(self, color: str):
        self._color = QColor(color)

    def set_stroke_width(self, width: int):
        self._stroke_width = width

    def set_opacity(self, opacity: int):
        """Set the background opacity (0-100, converted to 0-255 internally)."""
        self._opacity = int(opacity * 255 / 100)

    def clear(self):
        self._shapes.clear()
        self.update()

    def undo(self):
        if self._shapes:
            self._shapes.pop()
            self.update()

    def is_visible(self):
        return super().isVisible()

    def setVisible(self, visible: bool):
        super().setVisible(visible)
        if visible:
            self._update_geometry()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_drawing = True
            self._start_point = event.pos()
            if self._tool == DRAWING_TOOL_PEN:
                self._current_shape = {
                    "type": DRAWING_TOOL_PEN,
                    "color": self._color.name(),
                    "width": self._stroke_width,
                    "points": [event.pos()],
                }
            else:
                self._current_shape = {
                    "type": self._tool,
                    "color": self._color.name(),
                    "width": self._stroke_width,
                    "points": [self._start_point, event.pos()],
                }

    def mouseMoveEvent(self, event):
        self._cursor_pos = event.pos()
        self.update()
        if self._is_drawing and self._current_shape:
            pos = event.pos()
            if self._tool == DRAWING_TOOL_PEN:
                self._current_shape["points"].append(pos)
            else:
                self._current_shape["points"][1] = pos
            self.update()

    def mouseReleaseEvent(self, event):
        if self._is_drawing and self._current_shape:
            self._is_drawing = False
            pos = event.pos()

            if self._tool != DRAWING_TOOL_PEN:
                self._current_shape["points"][1] = pos

            if self._tool != DRAWING_TOOL_PEN or len(self._current_shape["points"]) > 1:
                self._shapes.append(self._current_shape)

            self._current_shape = None
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        # Draw background only if opacity > 0 (only affects background, not drawings)
        if self._opacity > 0:
            painter.fillRect(self.rect(), QColor(255, 255, 255, self._opacity))

        # Always draw cursor and shapes - they should be visible regardless of background opacity
        # Draw cursor dot
        cursor_color = QColor(self._color)
        cursor_color.setAlpha(255)
        painter.setPen(QPen(cursor_color, 2))
        painter.drawEllipse(self._cursor_pos, 3, 3)

        for shape in self._shapes:
            self._draw_shape(painter, shape)

        if self._current_shape:
            self._draw_shape(painter, self._current_shape)

        painter.end()

    def _draw_shape(self, painter, shape):
        color = QColor(shape["color"])
        color.setAlpha(255)  # Ensure full opacity
        width = shape["width"]
        points = shape["points"]
        shape_type = shape["type"]

        pen = QPen(color, width)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)

        if shape_type == DRAWING_TOOL_PEN:
            if len(points) < 2:
                return
            path = QPainterPath(points[0])
            for point in points[1:]:
                path.lineTo(point)
            painter.drawPath(path)

        elif shape_type == DRAWING_TOOL_LINE:
            if len(points) >= 2:
                painter.drawLine(points[0], points[1])

        elif shape_type == DRAWING_TOOL_RECT:
            if len(points) >= 2:
                rect = self._get_rect(points[0], points[1])
                painter.drawRect(rect)

        elif shape_type == DRAWING_TOOL_ELLIPSE:
            if len(points) >= 2:
                rect = self._get_rect(points[0], points[1])
                painter.drawEllipse(rect)

        elif shape_type == DRAWING_TOOL_ARROW:
            if len(points) >= 2:
                self._draw_arrow(painter, points[0], points[1])

    def _get_rect(self, p1, p2):
        return QRectF(p1.x(), p1.y(), p2.x() - p1.x(), p2.y() - p1.y())

    def _draw_arrow(self, painter, start, end):
        painter.drawLine(start, end)

        import math
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return

        arrow_size = painter.pen().width() * 4

        ux = dx / length
        uy = dy / length

        ax1 = end.x() - arrow_size * ux + arrow_size * 0.5 * uy
        ay1 = end.y() - arrow_size * uy - arrow_size * 0.5 * ux
        ax2 = end.x() - arrow_size * ux - arrow_size * 0.5 * uy
        ay2 = end.y() - arrow_size * uy + arrow_size * 0.5 * ux

        path = QPainterPath(end)
        path.moveTo(ax1, ay1)
        path.lineTo(end.x(), end.y())
        path.lineTo(ax2, ay2)
        painter.drawPath(path)
