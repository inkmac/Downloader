import traceback

from PySide6.QtCore import QThread, Signal
from yt_dlp import YoutubeDL

from src.utils.logger import YtLogger


class DownloadWorker(QThread):
    console_output = Signal(str)

    def __init__(
            self,
            url: str,
            cookie: str,
            fmt: str,
            output: str
    ):
        super().__init__()
        self.url = url
        self.cookie = cookie
        self.fmt = fmt
        self.output = output


    def run(self):
        try:
            self.download()
        except Exception as e:
            self.console_output.emit(f'[Exception] {str(e)}')
            traceback.print_exc()

    def download(self):
        ydl_opts = {
            'format': self.fmt,
            'cookiefile': str(self.cookie),
            'outtmpl': str(self.output),
            'logger': YtLogger(self.console_output),
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        self.console_output.emit("[Success] Download Complete")
