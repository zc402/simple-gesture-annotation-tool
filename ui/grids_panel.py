from PyQt5.QtWidgets import QWidget, QGridLayout
from ui.thumbnail_widget import ThumbnailWidget
import numpy as np


class GridsPanel(QWidget):
    """Grid layout containing multiple grids of video frame"""
    def __init__(self, num_row, num_column):
        super().__init__()
        self.__thumbs = []
        layout = QGridLayout()
        widget_idx = 0
        for y in range(num_row):
            for x in range(num_column):
                thumb = ThumbnailWidget(widget_idx)
                thumb.clicked.connect(lambda n=widget_idx: self.on_click(n))
                widget_idx = widget_idx + 1
                self.__thumbs.append(thumb)
                layout.addWidget(thumb, y, x)

        self.setLayout(layout)

    def set_img(self, widget_idx: int, img: np.ndarray):
        self.__thumbs[widget_idx].set_img(img)

    def set_label(self, widget_idx: int, text: str):
        self.__thumbs[widget_idx].set_label(text)

    def set_selected(self, widget_idx: int, is_selected: bool):
        """Set the selection state of a widget. """
        self.__thumbs[widget_idx].set_selection_border(is_selected)

    def set_blank(self, widget_idx: int):
        """Set ui response when no more image to show (end of video file)"""
        self.__thumbs[widget_idx].set_blank()

    # -----Methods need to be implemented outside
    def on_click(self, widget_idx):
        raise NotImplementedError()
