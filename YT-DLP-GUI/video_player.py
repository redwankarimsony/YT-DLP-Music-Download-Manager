from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.player = QMediaPlayer(self)

        # Replace with the path to your video file
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile('video.webm')))

        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)

        # Create play, pause, and stop buttons and connect them to the appropriate slots
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.player.play)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.player.pause)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.player.stop)

        # Create a layout and add the buttons and video widget to it
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)

app = QApplication([])

player = VideoPlayer()
player.show()

app.exec_()