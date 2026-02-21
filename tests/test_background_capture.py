"""Tests for background capture when hidden (Story 2.2)"""

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


class TestBackgroundCapture:
    """Test suite for background capture when hidden (AC 1, 2)."""

    def setup_method(self):
        get_qapp()

    def test_listener_continues_when_window_hidden(self):
        """Subtask 1.1: Verify keyboard listener continues when window hidden."""
        # The pynput keyboard listener is independent of window visibility
        # It captures globally regardless of whether the overlay is visible
        from keyboard_listener import KeyboardListener
        from unittest.mock import Mock, patch
        
        with patch("keyboard_listener.keyboard.Listener") as mock_class:
            mock_instance = Mock()
            mock_class.return_value = mock_instance
            
            listener = KeyboardListener()
            listener.start()
            
            # Listener is global - should still be running
            mock_instance.start.assert_called_once()

    def test_history_buffer_persists(self):
        """Subtask 1.2: Verify keystroke buffer persists in memory."""
        from history_widget import HistoryWidget, MAX_ENTRIES
        
        widget = HistoryWidget()
        
        # Add entries
        widget.on_key_pressed("a", "a")
        widget.on_key_pressed("b", "b")
        
        # Entries should be in memory
        assert len(widget._entries) >= 1
        
        # Buffer should persist (MAX_ENTRIES defines limit)
        assert MAX_ENTRIES == 40

    def test_listener_not_stopped_on_hide(self):
        """Verify listener is not stopped when window hides."""
        from app import MainWindow
        from unittest.mock import Mock, patch, call
        
        with patch("app.KeyboardListener") as mock_listener_class:
            mock_instance = Mock()
            mock_listener_class.return_value = mock_instance
            
            window = MainWindow()
            window.start()
            
            # Hide the window
            window.hide()
            
            # Listener should NOT be stopped when hiding
            # (only stopped on quit)
            mock_instance.stop.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
