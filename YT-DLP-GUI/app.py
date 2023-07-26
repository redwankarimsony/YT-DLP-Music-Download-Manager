# This Python file uses the following encoding: utf-8
import os
import sys

import requests
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QFrame, QFileDialog, QMainWindow, QComboBox, QPushButton, \
    QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QWidget, QMessageBox
from bs4 import BeautifulSoup

from ui_components import Ui_MainWindow, cfg, is_valid_youtube_playlist, SingleVideoWidget, Ui_Dialog
from yt_dlp_components import get_all_urls


def extract_playlist_link(link):
    """
    Extracts the playlist link from the given link
    :param link:    The link to extract the playlist link from
    :return:    The playlist link if found, None otherwise
    """
    parts = link.split("&")
    for part in parts:

        if part.startswith("list"):
            playlist_id = part.split("=")[-1]
            playlist_link = f"https://www.youtube.com/playlist?list={playlist_id}"

            return playlist_link
    else:
        return None


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.new_dialog = None
        self.download_btn = None
        self.video_codes = None
        self.download_link = None
        self.main_layout = None
        self.video_links = None
        self.playlist_link = None
        self.video_widgets = []
        self.setupUi(self)
        self.initUi()
        self.threadpool = QtCore.QThreadPool()

    def initUi(self):
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QtGui.QIcon(cfg.app_icon))
        self.resize(cfg.window_width, cfg.window_height)

        self.menuFile.triggered.connect(self.preferences_window)

        # making the central widget
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.addLayout(self.make_link_entry())

        self.download_link = None
        self.video_links = None
        self.video_codes = None

    def make_link_entry(self):
        """
        Creates the layout for the link entry
        :return:
        """
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.playlist_link = QLineEdit()
        self.playlist_link.setFont(cfg.font)
        self.playlist_link.setFixedHeight(cfg.link_height)
        self.playlist_link.setPlaceholderText("Enter Playlist Link")
        self.download_btn = QPushButton("Download")
        self.download_btn.setFont(cfg.font)
        self.download_btn.setFixedHeight(cfg.link_height)
        self.download_btn.clicked.connect(self.handle_download)

        layout.addWidget(self.playlist_link)
        layout.addWidget(self.download_btn)
        return layout

    def handle_download(self):
        """
        Handles the download button click
        :return:  None
        """
        for i in reversed(range(self.main_layout.count())):
            if isinstance(self.main_layout.itemAt(i).widget(), QFrame):
                self.main_layout.itemAt(i).widget().setParent(None)

        self.get_all_unique_codes()

    def show_popup_warning(self, title, message):
        """
        Shows a popup warning message
        :param title:       The title of the popup
        :param message:     The message to display
        :return:        None
        """
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def get_all_unique_codes(self):
        """
        Gets all the unique video codes from the playlist
        :return:    None
        """

        self.download_link = self.playlist_link.text()

        # extract the playlist link
        self.download_link = extract_playlist_link(self.download_link)
        if self.download_link is None:
            self.show_popup_warning("Error", "Not a valid youtube playlist. Please try another one.")
            return
        else:
            print("Playlist Link:", self.download_link)

        if is_valid_youtube_playlist(self.download_link):
            try:
                video_links = get_all_urls(playlist_url=self.download_link)
                codes = [x.split("=")[-1] for x in video_links]
                print("Number of Video Links Found: ", len(codes))
                print(codes)
                self.video_codes = codes
                self.video_links = video_links

                # Arrange all the video links in the scroll area
                self.main_layout.addWidget(self.get_scroll_area_widget())
            except Exception as ex:
                print("Exception Happened")
                print(str(ex))
                self.show_popup_warning("Error", "Not a valid youtube playlist. Please try another one.")

    def get_scroll_area_widget(self):
        """
        Creates the scroll area widget
        :return:   The scroll area widget
        """
        self.video_widgets = []
        container_widget = QFrame()
        # container_widget.setStyleSheet("border: 2px solid black;")
        layout = QVBoxLayout(container_widget)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        if len(self.video_links):
            for video_link in self.video_links:
                label = SingleVideoWidget(link=video_link, parent=container_widget)

                # thread work
                worker = Worker(get_video_thumbnail, video_link)
                worker.signals.finished.connect(label.set_thumbnail)
                worker.signals.video_title.connect(label.set_title)
                self.threadpool.start(worker)

                self.video_widgets.append(label)
                layout.addWidget(label)
                layout.addSpacing(3)

        # Set up the scroll area and add the container widget
        scroll_area.setWidget(container_widget)
        return scroll_area

    def preferences_window(self):
        """
        Opens the preferences window
        :return: None
        """
        print("Preferences Window")
        self.new_dialog = Dialog(self)
        self.new_dialog.exec_()


class Dialog(QDialog, Ui_Dialog):
    """
    The dialog window for the preferences menu in the File menu
    """
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)

        # Initial Configuration
        self.output_path_label.setText(cfg.default_download_path)
        self.concurrent_combo.addItems([f"    {str(x)}" for x in range(1, os.cpu_count())])
        self.audio_quality_combo.addItems([f"    {x}" for x in cfg.audio_quality])
        self.video_quality_combo.addItems([f"    {x}" for x in cfg.video_quality])
        self.audio_format_combo.addItems([f"    {x}" for x in cfg.audio_formats])
        self.video_format_combo.addItems([f"    {x}" for x in cfg.video_formats])

        # Setting the sytlesheet for the combo boxes
        self.concurrent_combo.setStyleSheet(cfg.combo_style)
        self.audio_format_combo.setStyleSheet(cfg.combo_style)
        self.audio_quality_combo.setStyleSheet(cfg.combo_style)
        self.video_format_combo.setStyleSheet(cfg.combo_style)
        self.video_quality_combo.setStyleSheet(cfg.combo_style)

        self.setFont(cfg.font_pref)
        for child in self.findChildren(QWidget):
            if isinstance(child, QPushButton):
                print("Found Push Button")
                child.setFont(cfg.font_pref)
            elif isinstance(child, QLabel):
                print("Found Label")
                child.setFont(cfg.font_pref)
            elif isinstance(child, QComboBox):
                print("Found Combo Box")
                child.setFont(cfg.font_pref)

        self.browse_btn.clicked.connect(self.open_folder_dialog)

    def open_folder_dialog(self):
        """
        Opens the folder dialog to select the output folder
        :return: None
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # To disable native dialogs on macOS
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)

        if folder_path:
            print("Selected Folder:", folder_path)
            self.output_path_label.setText(folder_path)


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    finished = pyqtSignal(QPixmap)
    video_title = pyqtSignal(str)


class Worker(QRunnable):
    """
    Worker thread
    """
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialize the runner function with passed args, kwargs.
        :return:
        """
        pixmap, title = self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit(pixmap)
        self.signals.video_title.emit(title)


def get_youtube_vidoe_id(video_link):
    """
    Gets the youtube video id from the given link
    :param video_link:  The youtube video link
    :return:    The video id
    """
    return video_link.split("=")[-1]


def get_video_thumbnail(video_link):
    """
    Gets the video thumbnail from the given video link
    :param video_link:
    :return:    The video thumbnail
    """
    video_id = get_youtube_vidoe_id(video_link)
    url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
    pixmap = load_image_from_url(url)

    title = get_youtube_video_title(video_link)

    return pixmap, title


def get_youtube_video_title(video_url):
    """
    Gets the youtube video title from the given video url
    :param video_url:  The youtube video url
    :return:    The video title
    """
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


def load_image_from_url(url):
    """
    Loads the image from the given url
    :param url:     The url to load the image from
    :return:        The image pixmap
    """
    response = requests.get(url)

    if response.status_code == 200:
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        return pixmap
    else:
        print("Error loading image from url")
        return None


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    # app.setStyleSheet(cfg.app_style)
    window.show()
    sys.exit(app.exec())
