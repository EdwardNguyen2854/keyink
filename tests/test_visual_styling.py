"""Tests for visual styling (Story 1.7)"""

import pytest
from PySide6.QtWidgets import QApplication


_app = None


def get_qapp():
    global _app
    if _app is None:
        _app = QApplication.instance()
        if _app is None:
            _app = QApplication([])
    return _app


class TestVisualStyling:
    """Test suite for visual styling (AC 1, 2, 3)."""

    def setup_method(self):
        get_qapp()

    def test_rounded_corners_in_styles(self):
        """Subtask 1.1: Verify border-radius is in styles."""
        from history_widget import _build_styles
        
        styles = _build_styles()
        
        # Check that border-radius is in the word style
        assert "border-radius" in styles["word"]

    def test_monospace_font_in_styles(self):
        """Subtask 3.1: Verify monospace font family is used."""
        from history_widget import _build_styles
        
        styles = _build_styles()
        
        # Check that monospace font is in the word style
        assert "monospace" in styles["word"].lower() or "consolas" in styles["word"].lower()

    def test_styles_module_exists(self):
        """Verify styles.py exists and has required colors."""
        import styles
        
        assert hasattr(styles, "BG_COLOR")
        assert hasattr(styles, "HISTORY_TEXT_COLOR")
        assert hasattr(styles, "ACCENT_COLOR")

    def test_special_key_style_exists(self):
        """Verify special key styling exists."""
        from history_widget import STYLE_SPECIAL, _build_styles
        
        styles = _build_styles()
        assert STYLE_SPECIAL in styles
        assert "font-size" in styles[STYLE_SPECIAL]

    def test_combo_style_exists(self):
        """Verify combo (modifier) styling exists."""
        from history_widget import STYLE_COMBO, _build_styles
        
        styles = _build_styles()
        assert STYLE_COMBO in styles
        assert "font-size" in styles[STYLE_COMBO]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
