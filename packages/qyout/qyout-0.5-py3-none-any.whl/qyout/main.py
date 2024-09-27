import sys
from PyQt6.QtWidgets import QApplication

from qyout.main_window import *


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # Start the event loop.
    app.exec()


if __name__ == "__main__":
    main()
