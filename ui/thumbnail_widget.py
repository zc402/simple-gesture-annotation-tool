from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


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
            # Set a border to indicate currently selected frame
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
