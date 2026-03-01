"""Main window — Professional Minimal aesthetic."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QAction
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSystemTrayIcon, QMenu, QLabel, QPushButton, QSizeGrip,
)

from history_widget import HistoryWidget
from keyboard_listener import KeyboardListener
from drawing_canvas import DrawingCanvas
from drawing_toolbar import DrawingToolbar
from settings import load_settings, save_settings
from settings_dialog import SettingsDialog
from styles import (
    BG_COLOR, ACCENT_COLOR, CLOSE_BTN_COLOR, CLOSE_BTN_HOVER, BORDER_COLOR, HISTORY_TEXT_COLOR,
    BG_SECONDARY, BORDER_HIGHTLIGHT,
)


class MainWindow(QMainWindow):
    """Frameless, always-on-top, semi-transparent overlay window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("KeyInk")
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(400, 360)
        self.setMinimumSize(280, 200)

        self._drag_pos = None
        self._settings = load_settings()

        # Central widget
        central = QWidget()
        central.setStyleSheet("background: transparent;")
        self.setCentralWidget(central)

        self._main_layout = QVBoxLayout(central)
        self._main_layout.setContentsMargins(12, 8, 12, 10)
        self._main_layout.setSpacing(0)

        # --- Title bar ---
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(4, 0, 0, 6)

        self._title_label = QLabel("KeyInk")
        self._title_label.setStyleSheet(
            f"color: {HISTORY_TEXT_COLOR}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; "
            f"font-size: 13px; font-weight: 500; background: transparent;"
        )
        self._title_label.setVisible(True)  # Explicit default
        title_bar.addWidget(self._title_label)
        title_bar.addStretch()

        # Minimize button
        self._minimize_btn = QPushButton("\u2014")
        self._minimize_btn.setFixedSize(24, 24)
        self._minimize_btn.setCursor(Qt.PointingHandCursor)
        self._minimize_btn.setStyleSheet(
            f"QPushButton {{ color: {CLOSE_BTN_COLOR}; background: transparent; border: none; "
            f"font-size: 14px; border-radius: 4px; }}"
            f"QPushButton:hover {{ color: {HISTORY_TEXT_COLOR}; background: {BG_SECONDARY}; }}"
        )
        self._minimize_btn.setVisible(True)  # Explicit default
        self._minimize_btn.clicked.connect(self._toggle_visibility)
        title_bar.addWidget(self._minimize_btn)

        # Settings button (gear icon)
        settings_btn = QPushButton("\u2699")
        settings_btn.setFixedSize(24, 24)
        settings_btn.setCursor(Qt.PointingHandCursor)
        settings_btn.setStyleSheet(
            f"QPushButton {{ color: {CLOSE_BTN_COLOR}; background: transparent; border: none; "
            f"font-size: 14px; border-radius: 4px; }}"
            f"QPushButton:hover {{ color: {HISTORY_TEXT_COLOR}; background: {BG_SECONDARY}; }}"
        )
        settings_btn.clicked.connect(self._open_settings)
        title_bar.addWidget(settings_btn)

        # Toggle drawing button
        draw_btn = QPushButton("✏")
        draw_btn.setFixedSize(24, 24)
        draw_btn.setCursor(Qt.PointingHandCursor)
        draw_btn.setStyleSheet(
            f"QPushButton {{ color: {CLOSE_BTN_COLOR}; background: transparent; border: none; "
            f"font-size: 12px; border-radius: 4px; }}"
            f"QPushButton:hover {{ color: {HISTORY_TEXT_COLOR}; background: {BG_SECONDARY}; }}"
        )
        draw_btn.clicked.connect(self._on_toggle_drawing)
        title_bar.addWidget(draw_btn)

        # Close button
        close_btn = QPushButton("\u2715")
        close_btn.setFixedSize(24, 24)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(
            f"QPushButton {{ color: {CLOSE_BTN_COLOR}; background: transparent; border: none; "
            f"font-size: 13px; border-radius: 4px; }}"
            f"QPushButton:hover {{ color: {CLOSE_BTN_HOVER}; background: {BG_SECONDARY}; }}"
        )
        close_btn.clicked.connect(self._quit)
        title_bar.addWidget(close_btn)

        self._main_layout.addLayout(title_bar)

        # --- Drawing toolbar ---
        self.drawing_toolbar = DrawingToolbar()
        self.drawing_toolbar.setVisible(False)
        self.drawing_toolbar.tool_selected.connect(self._on_tool_selected)
        self.drawing_toolbar.color_selected.connect(self._on_color_selected)
        self.drawing_toolbar.clear_clicked.connect(self._on_clear_drawing)
        self.drawing_toolbar.undo_clicked.connect(self._on_undo_drawing)
        self.drawing_toolbar.toggle_clicked.connect(self._on_toggle_drawing)
        self._main_layout.addWidget(self.drawing_toolbar)

        # --- History widget ---
        self.history_widget = HistoryWidget()
        self._main_layout.addWidget(self.history_widget, stretch=1)

        # --- Drawing canvas (must be before _apply_settings) ---
        self.drawing_canvas = DrawingCanvas()
        self.drawing_canvas.set_main_window(self)
        self.drawing_canvas.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowDoesNotAcceptFocus
        )
        self.drawing_canvas.hide()

        # Apply settings after all widgets are created
        self._apply_settings()

        # --- Resize grip ---
        grip_bar = QHBoxLayout()
        grip_bar.setContentsMargins(0, 4, 0, 0)
        grip_bar.addStretch()
        grip = QSizeGrip(self)
        grip.setFixedSize(14, 14)
        grip.setStyleSheet("background: transparent;")
        grip_bar.addWidget(grip)
        self._main_layout.addLayout(grip_bar)

        # Keyboard listener
        self.listener = KeyboardListener(self)
        self.listener.key_pressed.connect(self.history_widget.on_key_pressed)
        self.listener.key_released.connect(self.history_widget.on_key_released)
        self.listener.toggle_drawing.connect(self._on_toggle_drawing)
        self.listener.key_pressed.connect(self._on_key_pressed_drawing)

        # System tray
        self._setup_tray()

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.style().standardIcon(
            self.style().StandardPixmap.SP_ComputerIcon
        ))
        self.tray.setToolTip("KeyInk")

        menu = QMenu()
        menu.setStyleSheet(
            f"QMenu {{ background: {BG_COLOR}; color: {HISTORY_TEXT_COLOR}; "
            f"border: 1px solid {BORDER_COLOR}; border-radius: 8px; padding: 4px; }}"
            f"QMenu::item {{ padding: 6px 16px; border-radius: 4px; }}"
            f"QMenu::item:selected {{ background: {BG_SECONDARY}; }}"
        )

        toggle_action = QAction("Show / Hide", self)
        toggle_action.triggered.connect(self._toggle_visibility)
        menu.addAction(toggle_action)

        menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self._quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._toggle_visibility()

    def _toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()

    def _quit(self):
        self.listener.stop()
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()

    def start(self):
        self.listener.start()
        self.show()

    # --- Custom painting ---

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background - only draw if opacity > 0
        opacity = self._settings["opacity"] / 100.0
        if opacity > 0:
            bg = QColor(BG_COLOR)
            bg.setAlphaF(opacity)
            painter.setBrush(QBrush(bg))
            painter.setPen(QPen(QColor(BORDER_COLOR), 1))
            painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 8, 8)
        painter.end()

    # --- Context menu ---

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet(
            f"QMenu {{ background: {BG_COLOR}; color: {HISTORY_TEXT_COLOR}; "
            f"border: 1px solid {BORDER_COLOR}; border-radius: 8px; padding: 4px; }}"
            f"QMenu::item {{ padding: 6px 16px; border-radius: 4px; }}"
            f"QMenu::item:selected {{ background: {BG_SECONDARY}; }}"
        )

        settings_action = menu.addAction("Settings...")
        settings_action.triggered.connect(self._open_settings)

        draw_action = menu.addAction("Toggle Drawing")
        draw_action.triggered.connect(self._on_toggle_drawing)

        clear_action = menu.addAction("Clear History")
        clear_action.triggered.connect(self.history_widget.clear_history)

        menu.addSeparator()

        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self._quit)

        menu.exec(event.globalPos())

    def _open_settings(self):
        dlg = SettingsDialog(self._settings, self)
        if dlg.exec():
            self._settings = dlg.get_settings()
            save_settings(self._settings)
            self._apply_settings()
            self.update()

    def _apply_settings(self):
        self.history_widget.set_font_size(self._settings["font_size"])
        self.history_widget.set_show_special_keys(self._settings["show_special_keys"])
        self.history_widget.set_word_timeout(self._settings["word_timeout_ms"])

        # Apply canvas opacity using the history widget's set_opacity method
        canvas_opacity = self._settings.get("canvas_opacity", 100)
        self.history_widget.set_opacity(canvas_opacity)

        # Apply drawing overlay opacity
        drawing_opacity = self._settings.get("drawing_canvas_opacity", 15)
        self.drawing_canvas.set_opacity(drawing_opacity)

        # Apply drawing hotkey
        drawing_hotkey = self._settings.get("drawing_hotkey", "ctrl+shift+d")
        self.listener.set_drawing_hotkey(drawing_hotkey)

        # Apply minimal title bar
        minimal = self._settings.get("minimal_title_bar", False)
        self._title_label.setVisible(not minimal)
        self._minimize_btn.setVisible(not minimal)
        if minimal:
            # Adjust title bar margins when minimal
            self._main_layout.setContentsMargins(12, 4, 12, 10)
        else:
            self._main_layout.setContentsMargins(12, 8, 12, 10)

    def _on_tool_selected(self, tool):
        self.drawing_canvas.set_tool(tool)

    def _on_color_selected(self, color):
        self.drawing_canvas.set_color(color)

    def _on_clear_drawing(self):
        self.drawing_canvas.clear()

    def _on_undo_drawing(self):
        self.drawing_canvas.undo()

    def _on_toggle_drawing(self):
        if self.drawing_toolbar.isVisible():
            self.drawing_toolbar.setVisible(False)
            self.drawing_canvas.hide()
        else:
            self.drawing_toolbar.setVisible(True)
            self.drawing_canvas._update_geometry()
            self.drawing_canvas.show()

    def _on_key_pressed_drawing(self, key_id, display):
        if not self.drawing_toolbar.isVisible():
            return
        tool_map = {
            "1": "pen",
            "2": "rect",
            "3": "ellipse",
            "4": "arrow",
            "5": "line",
        }
        if key_id in tool_map:
            self._on_tool_selected(tool_map[key_id])
            self.drawing_toolbar.set_tool(tool_map[key_id])

    # --- Drag support ---

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def closeEvent(self, event):
        self.listener.stop()
        self.drawing_canvas.close()
        event.accept()
