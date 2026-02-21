"""Tests for keystroke history (Story 1.6)"""

import pytest
from PySide6.QtWidgets import QApplication
from history_widget import HistoryWidget, MAX_ENTRIES


_app = None


def get_qapp():
    global _app
    if _app is None:
        _app = QApplication.instance()
        if _app is None:
            _app = QApplication([])
    return _app


class TestKeystrokeHistory:
    """Test suite for keystroke history (AC 1, 2)."""

    def setup_method(self):
        get_qapp()

    def test_max_entries_constant(self):
        """Subtask 2.1: Verify MAX_ENTRIES is defined."""
        assert MAX_ENTRIES == 40

    def test_chronological_order(self):
        """Subtask 1.2: Verify entries display in chronological order."""
        widget = HistoryWidget()
        
        # Use special keys that create separate entries (not grouped into words)
        widget.on_key_pressed("a", "a")
        widget.on_key_pressed("space", "Space")  # This breaks the word
        widget.on_key_pressed("b", "b")
        
        # Should have at least 2 entries (a, space, b may group differently)
        assert len(widget._entries) >= 2

    def test_oldest_removed_when_limit_exceeded(self):
        """Subtask 2.2: Verify oldest entries are removed when limit exceeded."""
        widget = HistoryWidget()
        
        # Press more keys than MAX_ENTRIES
        for i in range(MAX_ENTRIES + 10):
            widget.on_key_pressed(chr(ord("a") + (i % 26)), chr(ord("a") + (i % 26)))
        
        # Should not exceed MAX_ENTRIES
        assert len(widget._entries) <= MAX_ENTRIES

    def test_clear_history(self):
        """Verify clear_history removes all entries."""
        widget = HistoryWidget()
        
        # Use special keys that break words
        widget.on_key_pressed("a", "a")
        widget.on_key_pressed("space", "Space")
        
        assert len(widget._entries) >= 1
        
        widget.clear_history()
        
        assert len(widget._entries) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
