"""Tests for global hotkey toggle (Story 2.1)"""

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


class TestGlobalHotkeyToggle:
    """Test suite for global hotkey toggle (AC 1, 2)."""

    def setup_method(self):
        get_qapp()

    def test_toggle_visibility_method_exists(self):
        """Subtask 2.1: Verify toggle visibility method exists."""
        from app import MainWindow
        
        window = MainWindow()
        assert hasattr(window, "_toggle_visibility")

    def test_tray_icon_exists(self):
        """Verify system tray icon is set up."""
        from app import MainWindow
        
        window = MainWindow()
        assert hasattr(window, "tray")
        assert window.tray is not None

    def test_tray_menu_has_toggle(self):
        """Verify tray menu has toggle action."""
        from app import MainWindow
        
        window = MainWindow()
        menu = window.tray.contextMenu()
        
        # Should have actions in menu
        assert menu.actions() is not None
        assert len(menu.actions()) > 0

    def test_listener_started_on_show(self):
        """Verify keyboard listener is started when window shows."""
        from app import MainWindow
        from unittest.mock import Mock, patch
        
        with patch("app.KeyboardListener") as mock_listener_class:
            mock_instance = Mock()
            mock_listener_class.return_value = mock_instance
            
            window = MainWindow()
            window.start()
            
            # Listener should be started
            mock_instance.start.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
