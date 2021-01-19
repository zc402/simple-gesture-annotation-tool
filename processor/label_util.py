import csv
from pathlib import Path
import numpy as np
import cv2


class LabelUtil:
    """Load, modify and save label"""
    def __init__(self, video_path):
        self.__video_path = video_path
        self.__csv_path = Path(video_path).with_suffix('.csv')
        self.__labels = self.__load()

    def update(self, first_idx, last_idx, label_str):
        self.__labels[first_idx: last_idx + 1] = label_str
        self.__save()
        pass

    def __getitem__(self, item):
        return self.__labels[item]

    def __load(self):

        cap = cv2.VideoCapture(self.__video_path)
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        if self.__csv_path.exists():
            with open(self.__csv_path, 'r', newline='') as csv_file:
                label_reader = csv.reader(csv_file)
                labels = list(label_reader)[0]
        else:
            # Create new csv file
            labels = ['0'] * num_frames

        if len(labels) != num_frames:
            raise ValueError('Video contains %d frames but csv contains %d labels' % (num_frames, len(labels)))
        labels = np.array(labels)
        return labels

    def __save(self):
        with open(self.__csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(list(self.__labels))

