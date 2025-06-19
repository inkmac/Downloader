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
        ydl_opts = {
            'format': self.fmt,
            'cookiefile': str(self.cookie),
            'outtmpl': str(self.output),
            'logger': YtLogger(self.console_output),
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            self.console_output.emit(f'[Exception] {str(e)}')
            return


