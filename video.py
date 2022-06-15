# APPLICATION FOR CAPTURING WEBCAM VIDEO STREAM

# LIBRARIES AND MODULES
# ---------------------

from PyQt5 import QtWidgets, uic # For the UI
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot # For threading and signaling between threads
from PyQt5.QtGui import QPixmap, QImage 
import cv2 # For image handling
import sys # For system parameters


# CLASS DEFINITIONS
# -----------------

# VIDEO THREAD
class VideoThread(QThread):

    # Constructor
    def __init__(self):
        super().__init__()
        self.alive = True # For stopping the video

    # Singal to interact with the main app
    changePixmap = pyqtSignal(QImage)

    # The runner function -> starts the thread, the name of the method must be run
    def run(self):
        videoStream = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Read the stream until stopped by the main app
        while self.alive:
            ret, frame = videoStream.read()

            # Check if there is a frame to process
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert from BGR to RGB
                height, width, channels = rgbImage.shape
                bytesPerLine = channels * width
                qtFormattedImage = QImage(
                    rgbImage.data,
                    width,
                    height,
                    bytesPerLine,
                    QImage.Format.Format_RGB888
                )
                self.changePixmap.emit(qtFormattedImage)

    def stop(self):
        self.alive = False



# APPLICATION (THREAD0)
class CaptureApp(QtWidgets.QMainWindow):

    # Constructor
    def __init__(self):
        super().__init__()

        uic.loadUi('video.ui', self)

        # Define UI elements
        self.videoImage = self.videoStreamLabel
        self.start = self.startVideoButton
        self.stop = self.stopVideoButton
        self.still = self.takeStillButton

        # Signals
        self.start.clicked.connect(self.startCapture)
        self.stop.clicked.connect(self.stopCapture)
        self.still.clicked.connect(self.takeStill)

        self.show()


    # Start capturing
    def startCapture(self):
        videoThread.alive = True
        videoThread.start() # Start method calls the run method of Qthread class
        videoThread.changePixmap.connect(self.setImage) # Connect to slot in the application


    # Stop capturing -> end thread
    def stopCapture(self):
        videoThread.stop()


    def takeStill(self):
        pass

    
    # Slots

    # Decorator function for catching video from the thread
    @pyqtSlot(QImage)
    def setImage(self, rgbImage):
        self.videoImage.setPixmap(QPixmap.fromImage(rgbImage))



if __name__ == '__main__':
    
    # Create the video thread -> videoThread object
    videoThread = VideoThread()

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = CaptureApp()
    app.exec_()
