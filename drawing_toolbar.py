"""Drawing toolbar widget."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QColor

from styles import BG_COLOR, ACCENT_COLOR, BORDER_COLOR, HISTORY_TEXT_COLOR


class DrawingToolbar(QWidget):
    tool_selected = Signal(str)
    color_selected = Signal(str)
    clear_clicked = Signal()
    undo_clicked = Signal()
    toggle_clicked = Signal()

    TOOL_BUTTONS = [
        ("pen", "1", "Pen"),
        ("rect", "2", "Rectangle"),
        ("ellipse", "3", "Ellipse"),
        ("arrow", "4", "Arrow"),
        ("line", "5", "Line"),
    ]

    COLORS = [
        ("#FF4444", "Red"),
        ("#4488FF", "Blue"),
        ("#44FF44", "Green"),
        ("#FFFF44", "Yellow"),
        ("#FFFFFF", "White"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_tool = "pen"
        self._current_color = "#FF4444"
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: transparent;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        tool_layout = QHBoxLayout()
        tool_layout.setSpacing(6)

        for tool_id, shortcut, tooltip in self.TOOL_BUTTONS:
            btn = QPushButton(shortcut)
            btn.setFixedSize(32, 28)
            btn.setToolTip(f"{tooltip} ({shortcut})")
            btn.clicked.connect(lambda checked, t=tool_id: self._on_tool_clicked(t))
            btn.setObjectName(f"tool_{tool_id}")
            tool_layout.addWidget(btn)

        tool_layout.addStretch()

        undo_btn = QPushButton("↩")
        undo_btn.setFixedSize(32, 28)
        undo_btn.setToolTip("Undo (Ctrl+Z)")
        undo_btn.clicked.connect(self.undo_clicked.emit)
        tool_layout.addWidget(undo_btn)

        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(32, 28)
        clear_btn.setToolTip("Clear (Ctrl+Shift+X)")
        clear_btn.clicked.connect(self.clear_clicked.emit)
        tool_layout.addWidget(clear_btn)

        toggle_btn = QPushButton("👁")
        toggle_btn.setFixedSize(32, 28)
        toggle_btn.setToolTip("Toggle Drawing")
        toggle_btn.clicked.connect(self.toggle_clicked.emit)
        tool_layout.addWidget(toggle_btn)

        layout.addLayout(tool_layout)

        color_layout = QHBoxLayout()
        color_layout.setSpacing(6)

        for color_hex, color_name in self.COLORS:
            btn = QPushButton()
            btn.setFixedSize(24, 24)
            btn.setStyleSheet(
                f"QPushButton {{ background-color: {color_hex}; "
                f"border: 2px solid {BORDER_COLOR}; border-radius: 4px; }}"
                f"QPushButton:hover {{ border: 2px solid {ACCENT_COLOR}; }}"
            )
            btn.setToolTip(color_name)
            btn.clicked.connect(lambda checked, c=color_hex: self._on_color_clicked(c))
            color_layout.addWidget(btn)

        color_layout.addStretch()

        layout.addLayout(color_layout)

        self._update_tool_buttons()

    def _on_tool_clicked(self, tool):
        self._current_tool = tool
        self._update_tool_buttons()
        self.tool_selected.emit(tool)

    def _on_color_clicked(self, color):
        self._current_color = color
        self.color_selected.emit(color)

    def _update_tool_buttons(self):
        for tool_id, _, _ in self.TOOL_BUTTONS:
            btn = self.findChild(QPushButton, f"tool_{tool_id}")
            if btn:
                if tool_id == self._current_tool:
                    btn.setStyleSheet(
                        f"QPushButton {{ background: {ACCENT_COLOR}; color: #000000; "
                        f"border: none; border-radius: 4px; font-weight: bold; }}"
                    )
                else:
                    btn.setStyleSheet(
                        f"QPushButton {{ background: {BORDER_COLOR}; color: {HISTORY_TEXT_COLOR}; "
                        f"border: none; border-radius: 4px; }}"
                        f"QPushButton:hover {{ background: #3a3a3a; }}"
                    )

    def set_tool(self, tool: str):
        self._current_tool = tool
        self._update_tool_buttons()

    def set_color(self, color: str):
        self._current_color = color
