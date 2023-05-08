import cv2


class Capture:
    def __init__(self, camera=0, resolution=(640, 480), framerate=30):
        self.camera = camera
        self.cap = cv2.VideoCapture(self.camera)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.cap.set(cv2.CAP_PROP_FPS, framerate)

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def __del__(self):
        self.release()

    def cascade(self, cascade_path):
        """
        Load cascade classifier from file.
        """
        return cv2.CascadeClassifier(cascade_path)

    def wait_key(self):
        return cv2.waitKey(1) & 0xFF

    def imshow(self, title, frame):
        cv2.imshow(title, frame)

    def gray(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
