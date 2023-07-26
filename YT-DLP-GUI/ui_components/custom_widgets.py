# This Python file uses the following encoding: utf-8
import os

import requests
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QRunnable, pyqtSlot, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFrame, QPushButton, QVBoxLayout, \
    QHBoxLayout, QWidget
from bs4 import BeautifulSoup

from yt_dlp_components import download_single_audio
from . import cfg


class SingleVideoWidget(QFrame):
    def __init__(self, link=None, parent=None, options=None):
        super().__init__(parent)
        self.worker = None
        self.thumbnail_label = None
        self.layout = None
        self.download_btn = None
        self.title_label = None
        self.link = link
        self.options = options
        self.initUi()

    def initUi(self):
        self.setFixedSize(1850, 210)

        self.layout = QHBoxLayout(self)
        self.thumbnail_label = QLabel()

        self.thumbnail_label.setFixedWidth(320)
        self.thumbnail_label.setFixedHeight(180)
        self.thumbnail_label.setAlignment(QtCore.Qt.AlignCenter)

        # id = self.get_youtube_vidoe_id(self.link)
        # thumbnail_url = self.get_youtube_thumbnail(id)
        # thumbnail = self.load_image_from_url(thumbnail_url)
        # self.thumbnail_label.setPixmap(thumbnail)

        self.title_label = VideoLinkTitle(self.link)
        self.download_btn = QPushButton("Download")
        self.download_btn.setFont(cfg.font)
        self.download_btn.setFixedWidth(180)
        self.download_btn.setFixedHeight(180)
        self.layout.addWidget(self.thumbnail_label, alignment=QtCore.Qt.AlignLeft)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.download_btn, alignment=QtCore.Qt.AlignRight)
        self.setStyleSheet("background-color: rgb(128, 128, 128);")

        self.worker = DownloadWorker(video_link=self.link, options=self.options)
        self.worker.finished.connect(self.handle_finished)

        self.download_btn.clicked.connect(self.handle_clicked)
        self.download_btn.setStyleSheet(cfg.download_btn_style2)

    def set_thumbnail(self, pixmap):
        self.thumbnail_label.setPixmap(pixmap)
        self.thumbnail_label.repaint()

    def set_title(self, title):
        self.title_label.title_label.setText(title)

    @staticmethod
    def get_youtube_thumbnail(video_id):
        return f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"

    @staticmethod
    def get_youtube_vidoe_id(video_link):
        return video_link.split("=")[-1]

    @staticmethod
    def load_image_from_url(url):
        response = requests.get(url)

        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            return pixmap
        else:
            print("Error loading image from url")
            return None

    def handle_clicked(self):
        print("Clicked Download button with link: ", self.link)
        self.download_btn.setEnabled(False)
        self.download_btn.setText("Downloading")
        self.worker.start()

    def handle_finished(self, result):
        print("Finished Downloading")
        self.download_btn.setText("Downloaded")
        self.download_btn.setEnabled(True)


class VideoLinkTitle(QWidget):
    def __init__(self, link=None):
        super().__init__()
        self.link_label = None
        self.title_label = None
        self.layout = None
        self.link = link
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.title_label = QLabel()
        self.title_label.setFont(cfg.font)
        self.link_label = QLabel()
        self.link_label.setFont(cfg.font)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.link_label)
        self.setStyleSheet("background-color: rgb(128, 128, 128);")

        self.link_label.setText(self.link)
        # self.title_label.setText(self.get_youtube_video_title(self.link))
        self.title_label.setText("Downloading...")

    @staticmethod
    def get_youtube_video_title(video_url):
        response = requests.get(video_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text()
                # The title usually contains the video title followed by " - YouTube"
                # We can remove " - YouTube" to get the actual video title.
                if " - YouTube" in title:
                    title = title.replace(" - YouTube", "")
                return title

        return None


class DownloadWorker(QThread):
    # Create a signal to be used for sending data to the main thread
    finished = pyqtSignal(str)

    def __init__(self, video_link, options=None):
        QThread.__init__(self)
        self.video_link = video_link
        self.options = options

    def run(self):
        # Long running task...
        print("Downloading Audio")
        command = ['yt-dlp',
                   '--embed-thumbnail',
                   '--audio-quality  0',
                   '-x',
                   '--audio-format  mp3',
                   "-o    '~/Music/CarSongs/%(title)s.%(ext)s'",
                   self.video_link]

        joined_command = " ".join(command)
        print(joined_command)
        os.system(joined_command)
        self.finished.emit("Download Finished in RUN")
