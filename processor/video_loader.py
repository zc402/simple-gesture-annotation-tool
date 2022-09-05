import cv2


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
                frame = cv2.resize(frame, (240, 240))
                self.__cached_frames.append(frame)
            else:
                break