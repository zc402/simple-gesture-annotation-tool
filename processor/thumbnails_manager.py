from processor.video_loader import VideoLoader
from processor.label_util import LabelUtil
import numpy as np


class ThumbnailsManager:
    """Manage the state of Thumbnail panel
    self.handle_select(widget_idx: int) accept idx of selected widget and change the state of this manager
    """
    def __init__(self, video_path, num_widgets, num_columns):

        self.__video_loader = VideoLoader(video_path)
        self.__label_utils = LabelUtil(video_path)
        # self.__thumb_widgets = thumbnail_widgets  # Thumbnail (image and label) widgets
        # for thumb in self.__thumb_widgets:
        #     thumb.clicked.connect(self.handle_select)
        self.__vidx_first_widget = 0  # The video index of first frame widget
        self.__clicks = []  # The video index of clicked (selected) images
        self.__interval = 1  # How many actual frames between two thumbnails

        self.num_widgets = num_widgets
        self.num_columns = num_columns

    def show_next(self):
        if self.__last_widget_idx() < self.__video_loader.num_frames - 1:
            self.__vidx_first_widget = self.__vidx_first_widget + \
                                       self.__interval * self.num_columns
            self.refresh_draw()
        else:
            print('End of the video')

    def show_previous(self):
        if self.__vidx_first_widget > 0:
            self.__vidx_first_widget = self.__vidx_first_widget - self.num_columns
        self.refresh_draw()

    def handle_click(self, widget_idx):
        """widget_index: index of clicked widget, for example 0~32"""
        video_idx = self.__video_idx(widget_idx)
        self.__clicks.append(video_idx)
        if len(self.__clicks) == 1:
            pass  # Do nothing, leave to the draw function
        elif len(self.__clicks) == 2:
            if self.__clicks[0] > self.__clicks[1]:
                # Let c[1] > c[0]
                self.__clicks.reverse()
            # Write into label and save
            # label_str = self.__receive_str()
            # self.__label_utils.update(self.__clicks[0], self.__clicks[1], label_str)
            # Unset selection border

        else:
            # clicks when two endpoints already set
            self.__clicks.clear()

        self.refresh_draw()

    def refresh_draw(self):
        """Set images, labels, selection borders onto the widget"""

        for w_idx in range(self.num_widgets):
            # Set images
            img = self.__video_loader[self.__video_idx(w_idx)]
            if img is None:
                self.on_EOF(w_idx)
                continue
            else:
                self.set_img(w_idx, img)

            # Set labels
            label_str = self.__label_utils[self.__video_idx(w_idx)]
            self.set_label(w_idx, label_str)

            # Clear selection border
            self.set_selected(w_idx, False)

        # Modify selection border for selected frames
        if len(self.__clicks) == 0:  # No selection
            return

        if len(self.__clicks) == 1:
            v_idx = self.__clicks[0]
            w_idx = self.__widget_idx(v_idx)
            if 0 <= w_idx < self.num_widgets:  # Inside the screen
                self.set_selected(w_idx, True)
        elif len(self.__clicks) == 2:
            # Select every grid between two clicks. c[0] < c[1].
            w_c0, w_c1 = [self.__widget_idx(v) for v in self.__clicks]
            for w_idx in range(w_c0, w_c1+1):
                if 0 <= w_idx < self.num_widgets:
                    self.set_selected(w_idx, True)

    def __widget_idx(self, video_idx):
        """Video idx to widget idx"""
        assert (video_idx - self.__vidx_first_widget) % self.__interval == 0
        return (video_idx - self.__vidx_first_widget) // self.__interval

    def __video_idx(self, widget_idx):
        """Widget idx to video idx"""
        return self.__vidx_first_widget + self.__interval * widget_idx

    def __last_widget_idx(self):
        return self.__vidx_first_widget + self.num_widgets - 1

    # ----------Methods must be implemented outside----------
    def set_img(self, widget_idx: int, img: np.ndarray):
        """Set the thumbnail image"""
        raise NotImplementedError()

    def set_label(self, widget_idx: int, text: str):
        raise NotImplementedError()

    def set_selected(self, widget_idx: int, is_selected: bool):
        """Set the selection state of a widget. """
        raise NotImplementedError()

    def on_EOF(self, widget_idx: int):
        """Set ui response when no more image to show (end of video file)"""
        raise NotImplementedError()
