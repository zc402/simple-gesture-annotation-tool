import os

from processor.thumbnails_manager import ThumbnailsManager
from ui.grids_panel import GridsPanel
from ui.main_window import MainW

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
from pathlib import Path
import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QDesktopWidget, QMainWindow, QAction, \
    QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon, QImage, QWheelEvent
from PyQt5.QtCore import pyqtSignal


class Configs:
    num_row = 4
    num_column = 8


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())
