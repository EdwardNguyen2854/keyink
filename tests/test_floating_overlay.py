"""Tests for floating overlay window (Story 1.4)"""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication


_app = None


def get_qapp():
    global _app
    if _app is None:
        _app = QApplication.instance()
        if _app is None:
            _app = QApplication([])
    return _app


class TestFloatingOverlayWindow:
    """Test suite for floating overlay window (AC 1)."""

    def setup_method(self):
        get_qapp()

    def test_frameless_window_flag(self):
        """Subtask 1.1: Verify frameless window flag is set."""
        from app import MainWindow
        
        window = MainWindow()
        flags = window.windowFlags()
        
        # Check frameless flag
        assert flags & Qt.FramelessWindowHint
        # Check always on top flag  
        assert flags & Qt.WindowStaysOnTopHint
        # Check tool flag (for overlay behavior)
        assert flags & Qt.Tool

    def test_window_title(self):
        """Subtask 1.1: Verify window has title."""
        from app import MainWindow
        
        window = MainWindow()
        assert window.windowTitle() == "Keystroke Viewer"

    def test_default_size(self):
        """Verify default window size is set."""
        from app import MainWindow
        
        window = MainWindow()
        size = window.size()
        # Default size is 420x400
        assert size.width() == 420
        assert size.height() == 400

    def test_minimum_size(self):
        """Verify minimum window size is enforced."""
        from app import MainWindow
        
        window = MainWindow()
        min_size = window.minimumSize()
        # Minimum size is 250x200
        assert min_size.width() == 250
        assert min_size.height() == 200


class TestNonIntrusiveDesign:
    """Test suite for non-intrusive overlay (AC 2)."""

    def setup_method(self):
        get_qapp()

    def test_tool_window_flag(self):
        """Subtask 3.1: Verify tool window flag for non-intrusive behavior."""
        from app import MainWindow
        
        window = MainWindow()
        flags = window.windowFlags()
        
        # Qt.Tool makes it a tool window that doesn't appear in taskbar
        assert flags & Qt.Tool

    def test_translucent_background(self):
        """Verify translucent background is enabled."""
        from app import MainWindow
        
        window = MainWindow()
        # WA_TranslucentBackground allows transparent background
        assert window.testAttribute(Qt.WA_TranslucentBackground)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
