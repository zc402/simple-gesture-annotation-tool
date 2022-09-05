from pathlib import Path


from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QWheelEvent, QIcon
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget, QMainWindow, QAction

from processor.thumbnails_manager import ThumbnailsManager
from ui.grids_panel import GridsPanel


class MainW(QMainWindow):

    def __init__(self):
        super().__init__()
        self.num_row = 3
        self.num_column = 6
        self.resize(512, 512)

        self.setWindowTitle('Center')
        self.statusBar().showMessage('StatusBar')
        openFile = QAction(QIcon('open.png'), 'Open', self)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        # noinspection PyUnresolvedReferences
        openFile.triggered.connect(self.__show_file_dialog)

        # TODO: This is a short cut for debugging
        # self.__init_grids(r'C:\Users\zc\Documents\005.mp4')
        self.show()

    def __to_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __show_file_dialog(self):
        home_dir = str(Path.home())
        file_path = QFileDialog.getOpenFileName(self, 'Open file', home_dir)[0]
        self.__init_grids(file_path)

    def __init_grids(self, file_path):
        self.grids_panel = GridsPanel(self.num_row, self.num_column)
        self.setCentralWidget(self.grids_panel)

        self.thumbs_manager = ThumbnailsManager(file_path, self.num_column * self.num_row, self.num_column)
        self.thumbs_manager.set_img = self.grids_panel.set_img
        self.thumbs_manager.set_label = self.grids_panel.set_label
        self.thumbs_manager.set_selected = self.grids_panel.set_selected
        self.thumbs_manager.on_EOF = self.grids_panel.set_blank
        self.thumbs_manager.set_sn = self.grids_panel.set_sn
        self.grids_panel.on_click = self.thumbs_manager.handle_click
        self.thumbs_manager.refresh_draw()

    def keyPressEvent(self, event):

        if self.thumbs_manager is None:
            event.ignore()
            return
        key = event.key()
        if Qt.Key_Space <= key <= Qt.Key_AsciiTilde:
            # handle ASCII char-like keys
            keyString = chr(key)
            print(keyString)
            self.thumbs_manager.handle_keypress(keyString)

    def wheelEvent(self, event: QWheelEvent):

        if self.thumbs_manager is None:
            event.ignore()
            return

        numPixels: QPoint = event.pixelDelta()
        numDegrees: QPoint = event.angleDelta() / 8

        if not numPixels.isNull():
            event.ignore()
        elif not numDegrees.isNull():
            num_steps: QPoint = numDegrees / 15  # .y() == Down: -1, Up: 1
            if num_steps.y() == -1:
                self.thumbs_manager.show_next()
                event.accept()
            elif num_steps.y() == 1:
                self.thumbs_manager.show_previous()
                event.accept()
            else:
                event.ignore()
