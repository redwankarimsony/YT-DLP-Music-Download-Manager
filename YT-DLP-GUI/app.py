# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QFrame, QFileDialog, QMainWindow, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QWidget

from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from ui_components import Ui_MainWindow, cfg, is_valid_youtube_playlist, SingleVideoWidget, Ui_Dialog
from yt_dlp_components import get_all_unique_codes, get_all_urls

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initUi()



    def initUi(self):
        self.setWindowTitle("Main Window")
        self.resize(cfg.window_width, cfg.window_height)

        self.menuFile.triggered.connect(self.preferences_window)    


    
        #making the central widget
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.addLayout(self.make_link_entry())
        

        self.download_link = None
        self.video_links = None
        self.video_codes = None



        


    def make_link_entry(self):
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.playlist_link = QLineEdit()
        self.playlist_link.setFont(cfg.font)
        self.playlist_link.setFixedHeight(cfg.link_height)
        self.playlist_link.setPlaceholderText("Enter Playlist Link")
        self.download_btn = QPushButton("Download")
        self.download_btn.setFont(cfg.font)
        self.download_btn.setFixedHeight(cfg.link_height)
        self.download_btn.clicked.connect(self.get_all_unique_codes)

        layout.addWidget(self.playlist_link)
        layout.addWidget(self.download_btn)
        return layout
    


    
    def get_all_unique_codes(self):
        self.download_link = self.playlist_link.text()
        if is_valid_youtube_playlist(self.download_link):
            try:
                video_links = get_all_urls(playlist_url = self.download_link)
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


    def get_scroll_area_widget(self):
        container_widget = QFrame()
        # container_widget.setStyleSheet("border: 2px solid black;")
        layout = QVBoxLayout(container_widget)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)


        if len(self.video_links):
            for video_link in self.video_links[:10]:
                label = SingleVideoWidget(link=video_link, parent=container_widget)
                layout.addWidget(label)
                layout.addSpacing(3)


        # Set up the scroll area and add the container widget
        
        scroll_area.setWidget(container_widget)
        
        return scroll_area
    


    def preferences_window(self):
        print("Preferences Window")
        self.new_dialog = Dialog(self)
        self.new_dialog.exec_()








        
class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)


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
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # To disable native dialogs on macOS
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)

        if folder_path:
            print("Selected Folder:", folder_path)
        












if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
