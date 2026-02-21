"""Tests for settings configuration (Stories 3-1 to 3-4)"""

import pytest
from PySide6.QtWidgets import QApplication
import os
import tempfile


_app = None


def get_qapp():
    global _app
    if _app is None:
        _app = QApplication.instance()
        if _app is None:
            _app = QApplication([])
    return _app


class TestSettingsConfiguration:
    """Test suite for settings configuration."""

    def setup_method(self):
        get_qapp()

    def test_settings_have_defaults(self):
        """Verify default settings exist."""
        from settings import DEFAULTS
        
        assert "opacity" in DEFAULTS
        assert "font_size" in DEFAULTS
        assert "word_timeout_ms" in DEFAULTS
        assert "show_special_keys" in DEFAULTS

    def test_settings_load(self):
        """Verify settings can be loaded."""
        from settings import load_settings
        
        settings = load_settings()
        assert isinstance(settings, dict)
        assert "opacity" in settings

    def test_settings_save(self):
        """Verify settings can be saved."""
        from settings import save_settings, load_settings
        
        # Save test settings
        test_settings = {"opacity": 75, "font_size": 20}
        save_settings(test_settings)
        
        # Load and verify
        loaded = load_settings()
        assert loaded["opacity"] == 75

    def test_settings_dialog_exists(self):
        """Verify settings dialog exists."""
        from settings_dialog import SettingsDialog
        from settings import load_settings
        
        settings = load_settings()
        dialog = SettingsDialog(settings)
        
        assert dialog is not None

    def test_apply_settings_method_exists(self):
        """Verify _apply_settings method exists."""
        from app import MainWindow
        
        window = MainWindow()
        assert hasattr(window, "_apply_settings")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
