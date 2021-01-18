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
from PyQt5.QtCore import QObject, pyqtSignal
import csv

class Configs:
    num_row = 4
    num_column = 8

class LabelUtils:
    """Load, modify and save label"""
    def __init__(self, video_path):
        self.__video_path = video_path
        self.__csv_path = Path(video_path).with_suffix('.csv')
        self.__labels = self.__load()

    def update(self, start, end, label_str):
        self.__labels[start: end] = label_str
        self.__save()
        pass

    def __getitem__(self, item):
        return self.__labels[item]

    def __load(self):
        if self.__csv_path.exists():
            with open(self.__csv_path, 'r', newline='') as csv_file:
                label_reader = csv.reader(csv_file)
                return list(label_reader)[0]
        else:
            # Create new csv file
            __cap = cv2.VideoCapture(self.__video_path)
            num_frames = int(__cap.get(cv2.CAP_PROP_FRAME_COUNT))
            labels = [0] * num_frames
            return labels

    def __save(self):
        with open(self.__csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.__labels)

    pass


class VideoLoader:
    """Load thumbnails (resized frames) from video progressively"""
    def __init__(self, video_path):
        self.__cap = cv2.VideoCapture(video_path)
        self.num_frames = int(self.__cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__cached_frames = []
        self.__add_size = 200

    def __getitem__(self, index):
        if index > self.num_frames - 1:
            return None  # No more frames, should display blank widget
        if index + 1 > len(self.__cached_frames):
            # Current frame not cached
            self.__cache_more()
            return self.__getitem__(index)
        return self.__cached_frames[index]

    def __del__(self):
        self.__cap.release()

    def __cache_more(self):

        for f in range(self.__add_size):
            ret, frame = self.__cap.read()
            if ret:
                frame = cv2.resize(frame, (128, 128))
                self.__cached_frames.append(frame)
            else:
                break


class GridWidgetsManager:
    """Manager of frame grids"""
    def __init__(self, thumbnail_widgets, video_path):
        self.__cache = VideoLoader(video_path)
        self.__thumb_widgets = thumbnail_widgets  # Thumbnail (image and label) widgets
        for thumb in self.__thumb_widgets:
            thumb.clicked.connect(self.__handle_thumb_click)
        self.__vidx_first_widget = 0  # The video index of first frame widget
        self.__clicks = []  # The video index of clicked (selected) images
        self.__interval = 1  # How many actual frames between two thumbnails

        self.__label_utils = LabelUtils(video_path)
        self.__refresh_draw()

    def show_next(self):
        if self.__last_widget_idx() < self.__cache.num_frames - 1:
            self.__vidx_first_widget = self.__vidx_first_widget + \
                                       self.__interval * Configs.num_column
            self.__refresh_draw()
        else:
            print('End of the video')

    def show_previous(self):
        if self.__vidx_first_widget > 0:
            self.__vidx_first_widget = self.__vidx_first_widget - Configs.num_column
        self.__refresh_draw()

    def __handle_thumb_click(self, widget_idx):
        """widget_index: index of clicked widget, always 0~32"""
        video_idx = self.__video_idx(widget_idx)
        self.__clicks.append(video_idx)
        if len(self.__clicks) == 1:
            pass  # Do nothing, leave to the draw function
        elif len(self.__clicks) == 2:
            if self.__clicks[0] > self.__clicks[1]:
                # Exchange
                self.__clicks.reverse()
            # Write into label and save
            # label_str = self.__receive_str()
            # self.__label_utils.update(self.__clicks[0], self.__clicks[1], label_str)
            # Unset selection border

        else:
            # clicks when two endpoints already set
            self.__clicks.clear()

        self.__refresh_draw()

    def __refresh_draw(self):
        """Set images, labels, selection borders onto the widget"""

        for w_idx, f in enumerate(self.__thumb_widgets):
            # Set images
            img = self.__cache[self.__video_idx(w_idx)]
            if img is None:
                f.set_blank()  # Set blank image and label
                continue
            else:
                f.set_img(img)

            # Set labels
            label_str = self.__label_utils[self.__video_idx(w_idx)]
            f.set_label(label_str)

        # Modify selection border for frames
        for f in self.__thumb_widgets:
            f.set_selection_border(False)
        if len(self.__clicks) == 0:  # No selection
            return

        if len(self.__clicks) == 1:
            v_idx = self.__clicks[0]
            w_idx = self.__widget_idx(v_idx)
            if 0 <= w_idx < len(self.__thumb_widgets):  # Inside the screen
                self.__thumb_widgets[w_idx].set_selection_border(True)
        elif len(self.__clicks) == 2:
            # Select every grid between two clicks. c[0] < c[1].
            w_c0, w_c1 = [self.__widget_idx(v) for v in self.__clicks]
            for w_idx in range(w_c0, w_c1+1):
                if 0 <= w_idx < len(self.__thumb_widgets):
                    self.__thumb_widgets[w_idx].set_selection_border(True)

    def __widget_idx(self, video_idx):
        """Video idx to widget idx"""
        assert (video_idx - self.__vidx_first_widget) % self.__interval == 0
        return (video_idx - self.__vidx_first_widget) // self.__interval

    def __video_idx(self, widget_idx):
        """Widget idx to video idx"""
        return self.__vidx_first_widget + self.__interval * widget_idx

    def __last_widget_idx(self):
        return self.__vidx_first_widget + len(self.__thumb_widgets) - 1

    def __receive_str(self):
        dialog = QLabel('Press a key to set label')
        dialog.show()
        return '1'


class ThumbnailWidget(QWidget):
    """Widget containing a thumbnail and a label of 1 video frame"""
    clicked = pyqtSignal(int)

    def __init__(self, widget_idx):
        super().__init__()
        self.widget_idx = widget_idx
        v_box = QVBoxLayout(self)
        v_box.setSpacing(0)
        v_box.setContentsMargins(0, 0, 0, 0)
        self.img_holder = QLabel(self)

        self.__label_holder = QLabel(text='?', parent=self)
        self.__label_holder.setStyleSheet("QLabel { background-color : rgb(200, 200, 200); color : black; }")
        self.__label_holder.setAlignment(Qt.AlignCenter)
        
        v_box.addWidget(self.img_holder)
        v_box.addWidget(self.__label_holder)

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        self.clicked.emit(self.widget_idx)

    def set_img(self, cv_img):
        qt_pix = self.__cv2qt(cv_img)
        self.img_holder.setPixmap(qt_pix)
        self.setVisible(True)

    def set_label(self, text: str):
        self.__label_holder.setText(text)

    def set_selection_border(self, selected: bool):
        if selected:
            # Set a border indicating currently selected frame
            self.setStyleSheet("border: 1px solid red")
        else:
            self.setStyleSheet("border: 1px solid white")

    def set_blank(self):
        self.setVisible(False)

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
        widget_idx = 0
        for y in range(Configs.num_row):
            for x in range(Configs.num_column):
                frame = ThumbnailWidget(widget_idx)
                widget_idx = widget_idx + 1
                self.frames.append(frame)
                layout.addWidget(frame, y, x)

        self.setLayout(layout)


class MainW(QMainWindow):

    def __init__(self):
        super().__init__()
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
        self.__init_grids(r'C:\Users\zc\PoliceGestureLong\train\001.mp4')
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
        self.grids = Grids()
        self.fwm = GridWidgetsManager(self.grids.frames, file_path)
        self.setCentralWidget(self.grids)

    def keyPressEvent(self, event):

        if self.fwm is None:
            event.ignore()
            return

        print(event.key())

    def wheelEvent(self, event: QWheelEvent):

        if self.fwm is None:
            event.ignore()
            return

        numPixels: QPoint = event.pixelDelta()
        numDegrees: QPoint = event.angleDelta() / 8

        if not numPixels.isNull():
            event.ignore()
        elif not numDegrees.isNull():
            num_steps: QPoint = numDegrees / 15  # .y() == Down: -1, Up: 1
            if num_steps.y() == -1:
                self.fwm.show_next()
                event.accept()
            elif num_steps.y() == 1:
                self.fwm.show_previous()
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