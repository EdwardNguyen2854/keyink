"""Entry point for the KeyInk application."""

import sys
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running in tray

    from app import MainWindow
    window = MainWindow()
    window.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
