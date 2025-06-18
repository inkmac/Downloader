from PySide6.QtWidgets import QMainWindow

from src.download_mainwindow import Ui_MainWindow


class Downloader(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # init
        self.init_state()
        self.connect_signals()


    def init_state(self):
        self.cmd_output_plaintextedit.setReadOnly(True)


    def connect_signals(self):
        self.video_download_button.clicked.connect(self.download_video)
        self.get_cookies_button.clicked.connect(self.get_cookies)

    # callback functions
    def get_cookies(self):
        browser = self.browser_combobox.currentText()
        website = self.website_combobox.currentText()




    def download_video(self):
        print("download_video")