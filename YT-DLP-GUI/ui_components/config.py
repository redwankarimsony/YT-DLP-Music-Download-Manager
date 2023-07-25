from PyQt5.QtGui import QFont
import os



class cfg:
    window_width = 1920
    window_height = 1080
    window_title = "Youtube MP3 Downloader"
    test_link = "https://www.youtube.com/playlist?list=PLx0sYbCqOb8QTF1DCJVfQrtWknZFzuoAE"
    link_height = 60
    app_icon = os.path.join(os.path.dirname(__file__), "assets/youtube_logo.png")

    # Create a font with specific properties
    font = QFont("Roboto", 16)
    font_pref = QFont("Roboto", 12)


    #audio formats
    audio_formats = ["mp3", "wav", "flac"]

    # audio quality
    audio_quality = ["128 kbps", "192 kbps", "256 kbps", "320 kbps"]

    # video formats
    video_formats = ["mp4", "mkv", "webm"]

    # video quality
    video_quality = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]

    # download path
    home_dir = os.path.expanduser("~")
    default_download_path = os.path.join(home_dir, "Music") # Get the path of the user's home directory

    combo_style ="""
                                    QComboBox {
                                        background-color: rgb(128, 128, 128);
                                        border: 2px solid rgb(240, 240, 240);
                                        border-radius: 5px;
                                        padding: 5px;
                                        text-align: center;
                                    }
                                    
                                    QComboBox::drop-down {
                                        subcontrol-origin: padding;
                                        subcontrol-position: right;
                                        width: 20px;
                                        border-left: 1px solid rgb(240, 240, 240);
                                        border-top-right-radius: 5px;
                                        border-bottom-right-radius: 5px;
                                        text-align: center;
                                    }
                                """
    
    app_style = stylesheet = """
    QMainWindow {
        background-color: #333;
    }
    
    QPushButton {
        background-color: #555;
        color: white;
        border-radius: 10px;
        padding: 5px;
        min-width: 100px;
        max-width: 300px;
        font-size: 18px;
    }

    QPushButton:hover {
        background-color: #777;
    }

    QPushButton:pressed {
        background-color: #999;
    }

    QLabel {
        color: white;
        font-size: 18px;
    }
    
    QTextEdit {
        background-color: #444;
        color: white;
        border-radius: 10px;
    }

    QLineEdit {
        background-color: #444;
        color: white;
        border-radius: 10px;
        padding: 5px;
    }

    QMenuBar {
        background-color: #222;
        color: white;
        border: none;
    }

    QMenuBar::item {
        background-color: #222;
        color: white;
    }

    QMenuBar::item:selected {
        background-color: #555;
    }

    QMenu {
        background-color: #222;
        color: white;
        border: none;
    }

    QMenu::item:selected {
        background-color: #555;
    }

    QComboBox {
        background-color: #444;
        color: white;
        border-radius: 10px;
        padding: 5px;
    }

    QComboBox:hover {
        background-color: #666;
    }

    QComboBox:editable {
        background-color: #444;
    }

    QComboBox QAbstractItemView {
        background-color: #444;
        color: white;
        selection-background-color: #888;
    }
"""

    download_btn_style = """
            QPushButton {
                color: #fff;
                background-color: #007BFF;
                border-radius: 4px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """


    download_btn_style2 = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;
    }
    QPushButton:hover {
        background-color: #66BB6A;
        color: white;
    }
    QPushButton:pressed {
        background-color: #2E7D32;
        color: white;
    }
"""






    
