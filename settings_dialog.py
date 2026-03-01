"""Settings dialog — Professional Minimal aesthetic."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox,
    QPushButton, QLineEdit,
)

from styles import (
    BG_COLOR, ACCENT_COLOR, BORDER_COLOR, HISTORY_TEXT_COLOR,
    BG_SECONDARY, BORDER_HIGHTLIGHT,
)

_DIALOG_STYLE = f"""
QDialog {{
    background-color: {BG_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
}}
QLabel {{
    color: {HISTORY_TEXT_COLOR};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 13px;
    background: transparent;
}}
QSlider::groove:horizontal {{
    height: 4px;
    background: {BG_SECONDARY};
    border-radius: 2px;
    margin: 8px 0;
}}
QSlider::handle:horizontal {{
    background: {ACCENT_COLOR};
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QSlider::sub-page:horizontal {{
    background: {ACCENT_COLOR};
    border-radius: 2px;
}}
QCheckBox {{
    color: {HISTORY_TEXT_COLOR};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 13px;
    spacing: 8px;
    background: transparent;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid {BORDER_HIGHTLIGHT};
    background: {BG_SECONDARY};
}}
QCheckBox::indicator:checked {{
    background: {ACCENT_COLOR};
    border-color: {ACCENT_COLOR};
}}
QPushButton {{
    color: {HISTORY_TEXT_COLOR};
    background: {BG_SECONDARY};
    border: 1px solid {BORDER_HIGHTLIGHT};
    border-radius: 6px;
    padding: 8px 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 13px;
}}
QPushButton:hover {{
    background: {BORDER_HIGHTLIGHT};
}}
QPushButton#okBtn {{
    background: {ACCENT_COLOR};
    color: #ffffff;
    font-weight: 500;
    border: none;
}}
QPushButton#okBtn:hover {{
    background: {ACCENT_COLOR};
    opacity: 0.9;
}}
QLineEdit {{
    color: {HISTORY_TEXT_COLOR};
    background: {BG_SECONDARY};
    border: 1px solid {BORDER_HIGHTLIGHT};
    border-radius: 6px;
    padding: 8px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 13px;
}}
QLineEdit:focus {{
    border: 1px solid {ACCENT_COLOR};
}}

"""


class SettingsDialog(QDialog):
    """Modal settings dialog."""

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setStyleSheet(_DIALOG_STYLE)

        self._settings = dict(settings)
        self._dialog_height = 600  # Base height
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Title
        title = QLabel("Settings")
        title.setStyleSheet(
            f"color: {HISTORY_TEXT_COLOR}; font-size: 16px; font-weight: 500;"
        )
        layout.addWidget(title)

        # Separator
        sep = QLabel()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background: {BORDER_COLOR};")
        layout.addWidget(sep)

        # Font size
        self._font_size_label = QLabel()
        self._font_slider = self._make_slider(14, 48, self._settings["font_size"])
        self._font_slider.valueChanged.connect(self._on_font_size_changed)
        self._on_font_size_changed(self._settings["font_size"])
        layout.addWidget(self._font_size_label)
        layout.addWidget(self._font_slider)

        # Opacity (window background)
        self._opacity_label = QLabel()
        self._opacity_slider = self._make_slider(0, 100, self._settings["opacity"])
        self._opacity_slider.valueChanged.connect(self._on_opacity_changed)
        self._on_opacity_changed(self._settings["opacity"])
        layout.addWidget(self._opacity_label)
        layout.addWidget(self._opacity_slider)

        # Word grouping speed
        self._timeout_label = QLabel()
        self._timeout_slider = self._make_slider(100, 1000, self._settings["word_timeout_ms"])
        self._timeout_slider.valueChanged.connect(self._on_timeout_changed)
        self._on_timeout_changed(self._settings["word_timeout_ms"])
        layout.addWidget(self._timeout_label)
        layout.addWidget(self._timeout_slider)

        # Show special keys
        self._special_cb = QCheckBox("Show special keys (Space, Enter, Backspace...)")
        self._special_cb.setChecked(self._settings["show_special_keys"])
        layout.addWidget(self._special_cb)

        # Minimal title bar
        self._minimal_title_bar_cb = QCheckBox("Minimal title bar (title + close only)")
        self._minimal_title_bar_cb.setChecked(self._settings["minimal_title_bar"])
        layout.addWidget(self._minimal_title_bar_cb)

        # Canvas opacity
        self._canvas_opacity_label = QLabel()
        self._canvas_opacity_slider = self._make_slider(0, 100, self._settings["canvas_opacity"])
        self._canvas_opacity_slider.valueChanged.connect(self._on_canvas_opacity_changed)
        self._on_canvas_opacity_changed(self._settings["canvas_opacity"])
        layout.addWidget(self._canvas_opacity_label)
        layout.addWidget(self._canvas_opacity_slider)

        # Drawing overlay canvas opacity
        self._drawing_opacity_label = QLabel()
        self._drawing_opacity_slider = self._make_slider(1, 100, self._settings.get("drawing_canvas_opacity", 15))
        self._drawing_opacity_slider.valueChanged.connect(self._on_drawing_opacity_changed)
        self._on_drawing_opacity_changed(self._settings.get("drawing_canvas_opacity", 15))
        layout.addWidget(self._drawing_opacity_label)
        layout.addWidget(self._drawing_opacity_slider)

        # Drawing hotkey
        hotkey_label = QLabel("Drawing toggle hotkey:")
        layout.addWidget(hotkey_label)

        self._hotkey_input = QLineEdit(self._settings.get("drawing_hotkey", "ctrl+shift+d"))
        self._hotkey_input.setPlaceholderText("e.g., ctrl+shift+d")
        layout.addWidget(self._hotkey_input)

        hotkey_hint = QLabel("Use format: modifier+key (e.g., ctrl+shift+d)")
        hotkey_hint.setStyleSheet("font-size: 11px; color: #888;")
        layout.addWidget(hotkey_hint)

        layout.addStretch()

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        ok_btn = QPushButton("OK")
        ok_btn.setObjectName("okBtn")
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.clicked.connect(self._on_ok)
        btn_row.addWidget(ok_btn)

        layout.addLayout(btn_row)

    def _make_slider(self, min_val, max_val, value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(value)
        return slider

    def _on_font_size_changed(self, val):
        self._font_size_label.setText(f"Font size: {val}px")

    def _on_opacity_changed(self, val):
        self._opacity_label.setText(f"Window opacity: {val}%")

    def _on_timeout_changed(self, val):
        self._timeout_label.setText(f"Word grouping speed: {val}ms")

    def _on_canvas_opacity_changed(self, val):
        self._canvas_opacity_label.setText(f"Canvas opacity: {val}%")

    def _on_drawing_opacity_changed(self, val):
        self._drawing_opacity_label.setText(f"Drawing overlay opacity: {val}%")

    def _on_ok(self):
        self._settings["font_size"] = self._font_slider.value()
        self._settings["opacity"] = self._opacity_slider.value()
        self._settings["canvas_opacity"] = self._canvas_opacity_slider.value()
        self._settings["drawing_canvas_opacity"] = max(1, self._drawing_opacity_slider.value())
        self._settings["minimal_title_bar"] = self._minimal_title_bar_cb.isChecked()
        self._settings["word_timeout_ms"] = self._timeout_slider.value()
        self._settings["show_special_keys"] = self._special_cb.isChecked()
        self._settings["drawing_hotkey"] = self._hotkey_input.text().strip().lower()
        self.accept()

    def get_settings(self):
        return dict(self._settings)
