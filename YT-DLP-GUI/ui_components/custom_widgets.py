# This Python file uses the following encoding: utf-8
import sys
import requests
from PyQt5.QtWidgets import QApplication,QLabel, QFrame, QMainWindow, QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QWidget

from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from bs4 import BeautifulSoup
from . import cfg


class SingleVideoWidget(QFrame):
    def __init__(self, link=None, parent=None):
        super().__init__(parent)
        self.link = link
        self.initUi()



    def initUi(self):
        self.setFixedSize(1850, 210)

        
        self.layout = QHBoxLayout(self)
        self.thumbnail_label = QLabel()
        
        
        self.thumbnail_label.setFixedWidth(320)
        self.thumbnail_label.setFixedHeight(180)

        id = self.get_youtube_vidoe_id(self.link)
        thumbnail_url = self.get_youtube_thumbnail(id)
        thumbnail = self.load_image_from_url(thumbnail_url)
        print(thumbnail.width(), thumbnail.height(), self.thumbnail_label.width(), self.thumbnail_label.height())   
        self.thumbnail_label.setAlignment(QtCore.Qt.AlignCenter)
        self.thumbnail_label.setPixmap(thumbnail)







        self.title_label = VideoLinkTitle(self.link)
        self.download_btn = QPushButton("Download")
        self.download_btn.setFont(cfg.font) 
        self.download_btn.setFixedWidth(180)
        self.download_btn.setFixedHeight(180)
        self.layout.addWidget(self.thumbnail_label)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.download_btn)

        # self.title_label.setText(self.link)

        self.setStyleSheet("background-color: rgb(128, 128, 128);")

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
        


    


class VideoLinkTitle(QWidget):
    def __init__(self, link=None):
        super().__init__()
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
        self.title_label.setText(self.get_youtube_video_title(self.link))     


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

    

        
        