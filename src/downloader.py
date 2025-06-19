from PySide6.QtWidgets import QMainWindow

from settings import COOKIES_DIR, VIDEOS_DIR
from src.ui.download_mainwindow import Ui_MainWindow
from src.utils.cookie import CookieWorker
from src.utils.download import DownloadWorker


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
        # get params
        url = self.video_url_lineedit.text()
        fmt = self.video_format_lineedit.text()

        if 'bilibili.com' in url:
            cookie = COOKIES_DIR / 'bilibili.com_cookies.txt'
            output = VIDEOS_DIR / 'bilibili' / '%(title)s.%(ext)s'
        elif 'youtube.com' in url:
            cookie = COOKIES_DIR / 'youtube.com_cookies.txt'
            output = VIDEOS_DIR / 'youtube' / '%(title)s.%(ext)s'
        else:
            self.cmd_output_plaintextedit.appendPlainText('当前网址不支持！')
            return

        if not cookie.exists():
            self.cmd_output_plaintextedit.appendPlainText('该网址cookie不存在！请先获取cookies！')
            return

        output.parent.mkdir(parents=True, exist_ok=True)

        # start worker
        self.download_worker = DownloadWorker(
            url=url,
            cookie=cookie,
            fmt=fmt,
            output=output,
        )
        self.download_worker.result_ready.connect(self.on_download_output_message)
        self.download_worker.start()


    def on_download_output_message(self, message: str):
        self.cmd_output_plaintextedit.appendPlainText(message)

