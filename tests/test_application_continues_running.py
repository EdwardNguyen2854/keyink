"""Tests for application continues running (Story 2.3)"""

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


class TestApplicationContinuesRunning:
    """Test suite for application continues running (AC 1, 2)."""

    def setup_method(self):
        get_qapp()

    def test_system_tray_icon_exists(self):
        """Subtask 1.1: Verify system tray integration exists."""
        from app import MainWindow
        
        window = MainWindow()
        assert hasattr(window, "tray")
        assert window.tray is not None

    def test_tray_shows_tooltip(self):
        """Verify tray icon has tooltip."""
        from app import MainWindow
        
        window = MainWindow()
        tooltip = window.tray.toolTip()
        assert "Keystroke" in tooltip

    def test_tray_context_menu_exists(self):
        """Subtask 1.1: Verify tray context menu exists."""
        from app import MainWindow
        
        window = MainWindow()
        menu = window.tray.contextMenu()
        assert menu is not None
        assert len(menu.actions()) > 0

    def test_toggle_immediate_show(self):
        """Subtask 2.1: Verify toggle shows window immediately."""
        from app import MainWindow
        
        window = MainWindow()
        
        # Hide window first
        window.hide()
        assert not window.isVisible()
        
        # Toggle should show immediately
        window._toggle_visibility()
        assert window.isVisible()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
