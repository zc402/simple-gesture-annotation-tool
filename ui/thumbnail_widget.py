from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedLayout, QFrame

from ui.color_palette import ColorPalette


class ThumbnailWidget(QFrame):
    """Widget containing a thumbnail and a label of 1 video frame"""
    clicked = pyqtSignal(int)

    def __init__(self, widget_idx):
        super().__init__()
        self.__widget_idx = widget_idx

        v_box = QVBoxLayout(self)
        v_box.setSpacing(0)
        v_box.setContentsMargins(0, 0, 0, 0)
        self.__img_holder = QLabel(self)
        self.__img_holder.setStyleSheet("QLabel { border: 0px;}")

        self.__label_holder = QLabel(text='?')
        self.__label_holder.setStyleSheet("QLabel { background-color : rgb(200, 200, 200); color : black; border: 0px;}")
        self.__label_holder.setAlignment(Qt.AlignCenter)

        self.__sn_holder = QLabel(text='00000')
        self.__sn_holder.setAlignment(Qt.AlignTop)
        self.__sn_holder.setStyleSheet("QLabel { background-color : rgb(0, 0, 0, 128); color : white; border: 0px;}")
        br = self.__sn_holder.fontMetrics().boundingRect('00000')
        self.__sn_holder.setFixedSize(br.width(), br.height())

        stackedLayout = QStackedLayout()  # Stack image and sn, label
        stackedLayout.setStackingMode(QStackedLayout.StackAll)  # All widgets are visible
        stackedLayout.addWidget(self.__img_holder)
        stackedLayout.addWidget(self.__sn_holder)

        v_box.addLayout(stackedLayout)
        v_box.addWidget(self.__label_holder)

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        self.clicked.emit(self.__widget_idx)

    def set_img(self, cv_img):
        qt_pix = self.__cv2qt(cv_img)
        self.__img_holder.setPixmap(qt_pix)
        self.setVisible(True)

    def set_label(self, text: str):
        self.__label_holder.setText(text)
        color_style = "QLabel {background-color : rgb(%d, %d, %d); border: 0px;}" % tuple(ColorPalette.get_rgb(text))
        self.__label_holder.setStyleSheet(color_style)

    def set_selection_border(self, selected: bool):
        if selected:
            # Set a border to indicate currently selected frame
            self.setStyleSheet("QFrame {border: 1px solid red}")
        else:
            self.setStyleSheet("QFrame {border: 1px solid white}")

    def set_blank(self):
        self.setVisible(False)

    def set_sn(self, num: int):
        self.__sn_holder.setText(str(num))

    @staticmethod
    def __cv2qt(cv_img):
        """Convert from an opencv image to QPixmap"""
        height, width, channel = cv_img.shape
        bytesPerLine = 3 * width
        qImg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_BGR888)
        qPix = QPixmap(qImg)
        return qPix
