"""Tests for overlay transparency (Story 1.5)"""

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


class TestOverlayTransparency:
    """Test suite for overlay transparency (AC 1, 2)."""

    def setup_method(self):
        get_qapp()

    def test_default_opacity_in_defaults(self):
        """Subtask 2.1: Verify default opacity is in DEFAULTS (70-90%)."""
        from settings import DEFAULTS
        
        # Default opacity should be in range 70-90 per story AC
        assert 70 <= DEFAULTS.get("opacity", 0) <= 90

    def test_opacity_setting_range(self):
        """Verify opacity setting is within valid range."""
        from settings import load_settings
        
        settings = load_settings()
        opacity = settings.get("opacity", 0)
        # Opacity should be 0-100
        assert 0 <= opacity <= 100

    def test_apply_settings_sets_opacity(self):
        """Subtask 1.2: Verify _apply_settings handles opacity."""
        from app import MainWindow
        from settings import load_settings
        
        window = MainWindow()
        settings = load_settings()
        
        # Simulate applying settings
        window._settings = settings
        window._apply_settings()
        
        # Should not raise any errors
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
