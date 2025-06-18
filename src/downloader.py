from PySide6.QtWidgets import QMainWindow

from src.ui.download_mainwindow import Ui_MainWindow
from src.utils.cookie import CookieWorker


class Downloader(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # init
        self.init_state()
        self.connect_signals()


    def init_state(self):
        self.cmd_output_plaintextedit.setReadOnly(True)
        self.get_cookie_result_plaintextedit.setReadOnly(True)

    def connect_signals(self):
        self.get_cookies_button.clicked.connect(self.get_cookies)
        self.video_download_button.clicked.connect(self.download_video)

    # callback functions
    def get_cookies(self):
        browser = self.browser_combobox.currentText()
        website = self.website_combobox.currentText()

        self.cookie_worker = CookieWorker(website, browser)
        self.cookie_worker.result_ready.connect(self.on_cookie_get_done)
        self.cookie_worker.start()

    def on_cookie_get_done(self, result: str):
        self.get_cookie_result_plaintextedit.setPlainText(result)


    def download_video(self):
        print("download_video")