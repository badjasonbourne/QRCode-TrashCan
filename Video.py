import cv2 as cv
from threading import Thread


class Video(object):

    def __init__(self):
        self.stream = cv.VideoCapture(0)
        (self.ret, self.frame) = self.stream.read()
        self.detector = cv.QRCodeDetector()
        self.item = None

    def start(self):
        Thread(target=self.detect, args=()).start()
        return self

    def detect(self):
        while True:
            self.ret, self.frame = self.stream.read()
            frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
            frame = cv.resize(frame, (100,100))
            points = self.detector.detect(frame)
            if points[0]:
                inf = self.detector.decode(frame, points[1])
                self.item = inf[0]
                if self.item != '':
                   pass

