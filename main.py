import os
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
from pathlib import Path
import cv2
import numpy as np
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QDesktopWidget, QMainWindow, QAction, \
    QFileDialog, QHBoxLayout, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QColor, QIcon, QImage, QWheelEvent


class ThumbnailCache:
    """Save thumbnails (resized frames) from video"""
    def __init__(self, video_path):
        self.__cap = cv2.VideoCapture(r'C:\Users\zc\PoliceGestureLong\train\001.mp4')
        self.num_frames = 200# int(self.__cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__frames = []  # TODO: Optimize
        for f in range(200):
            ret, frame = self.__cap.read()
            frame = cv2.resize(frame, (128, 128))
            self.__frames.append(frame)

    def __getitem__(self, index):
        return self.__frames[index]

    def __del__(self):
        self.__cap.release()


class FrameStateManager:
    """Manager of frame grids"""
    def __init__(self, frame_list):
        self.__cache = None
        self.__frames = frame_list
        self.__first_idx = 0  # The index of first image inside grid layout
        self.__clicks = []  # Save frame index of clicked images

    def load_video(self, file_path):
        self.__cache = ThumbnailCache(file_path)
        self.__load_csv()
        self.__first_idx = 0
        self.__refresh_draw()

    def show_next(self):
        # TODO: what if next() adds more than 1 frame
        if self.__last_idx() < self.__cache.num_frames - 1:
            self.__first_idx = self.__first_idx + 1
            self.__refresh_draw()
        else:
            print('End of the video')


    def show_previous(self):
        if self.__first_idx > 0:
            self.__first_idx = self.__first_idx - 1
        self.__refresh_draw()

    def handle_frame_click(self, index: int):
        self.__clicks.append(index)
        if len(self.__clicks) == 1:
            pass
        elif len(self.__clicks) == 2:
            # Write into label and save
            self.__save_csv()
            # Unset selection border
            self.__clicks.clear()
        else:
            raise ValueError('Unexpected click list len: %d' % len(self.__clicks))
        self.__refresh_draw()

    def __refresh_draw(self):
        """Set images, labels, selection borders onto the widget"""
        # Set images
        for ind, f in enumerate(self.__frames):
            img = self.__cache[self.__first_idx + ind]
            f.set_img(img)
        # Set labels
        # Set selection border for clicked frame
        if len(self.__clicks) == 1:
            selected_ind = self.__clicks[0]
            frame_widget = self.__frames[self.__widget_index(selected_ind)]
            frame_widget.set_selection_border()
        else:
            for f in self.__frames:
                f.unset_selection_border()

    def __widget_index(self, frame_index):
        return frame_index - self.__first_idx

    def __load_csv(self):
        pass

    def __save_csv(self):
        pass

    def __last_idx(self):
        return self.__first_idx + len(self.__frames) - 1

class Frame(QWidget):
    # one frame in video and it's label
    def __init__(self):
        super().__init__()
        v_box = QVBoxLayout(self)
        v_box.setSpacing(0)
        v_box.setContentsMargins(0,0,0,0)
        self.img_holder = QLabel(self)

        self.label_holder = QLabel(text='?', parent=self)
        self.label_holder.setStyleSheet("QLabel { background-color : rgb(200, 200, 200); color : black; }")
        
        v_box.addWidget(self.img_holder)
        v_box.addWidget(self.label_holder)

    def set_img(self, cv_img):
        qt_pix = self.__cv2qt(cv_img)
        self.img_holder.setPixmap(qt_pix)

    def set_label(self, text: str):
        self.label_holder.setText(text)

    def set_selection_border(self):
        """A border indicating currently selected frame"""

    def unset_selection_border(self):
        pass

    @staticmethod
    def __cv2qt(cv_img):
        """Convert from an opencv image to QPixmap"""
        height, width, channel = cv_img.shape
        bytesPerLine = 3 * width
        qImg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_BGR888)
        qPix = QPixmap(qImg)
        return qPix


class Grids(QWidget):
    """Grid layout containing multiple grids of video frame"""
    def __init__(self):
        super().__init__()
        self.frames = []
        layout = QGridLayout()
        index = 0
        for y in range(4):
            for x in range(8):
                frame = Frame()
                index = index + 1
                self.frames.append(frame)
                layout.addWidget(frame, y, x)

        self.setLayout(layout)

class MainW(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(512, 512)
        self.__to_center()
        self.setWindowTitle('Center')
        self.statusBar().showMessage('StatusBar')
        openFile = QAction(QIcon('open.png'), 'Open', self)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.grids = Grids()
        self.fsm = FrameStateManager(self.grids.frames)
        openFile.triggered.connect(self.fsm.load_video)  # self.show_file_dialog

        self.setCentralWidget(self.grids)
        self.show()

    def __to_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __show_file_dialog(self):
        home_dir = str(Path.home())
        file_path = QFileDialog.getOpenFileName(self, 'Open file', home_dir)[0]
        print(file_path)

    def keyPressEvent(self, event):
        print(event.key())

    def wheelEvent(self, event: QWheelEvent):

        numPixels: QPoint = event.pixelDelta()
        numDegrees: QPoint = event.angleDelta() / 8

        if not numPixels.isNull():
            event.ignore()
        elif not numDegrees.isNull():
            num_steps: QPoint = numDegrees / 15  # .y() == Down: -1, Up: 1
            if num_steps.y() == -1:
                self.fsm.show_next()
                event.accept()
            elif num_steps.y() == 1:
                self.fsm.show_previous()
                event.accept()
            else:
                event.ignore()



def main():

    app = QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


# cap = cv2.VideoCapture(r'C:\Users\zc\PoliceGestureLong\train\001.mp4')
# ind = 0
# thumbnails = []
# while True:
#     ret, frame = cap.read()
#     if ret:
#         b = cv2.resize(frame, (256, 256))
#         thumbnails.append(b)
#         ind = ind + 1
#         print(ind)
#     else:
#         break
#
# cap.release()
# cv2.destroyAllWindows()

if __name__ == '__main__':
    main()