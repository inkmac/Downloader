import traceback
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from yt_dlp import YoutubeDL

from src.utils.logger import YtLogger


class DownloadWorker(QThread):
    console_output = Signal(str)

    def __init__(
            self,
            url: str,
            fmt: str,
            outtmpl: Path,
            cookiefile: Path = None,
    ):
        super().__init__()
        self.url = url
        self.fmt = fmt
        self.outtmpl = outtmpl
        self.cookiefile = cookiefile


    def run(self):
        try:
            self.download()
        except Exception as e:
            self.console_output.emit(f'[Exception] {str(e)}')
            traceback.print_exc()

    def download(self):
        self.outtmpl.parent.mkdir(parents=True, exist_ok=True)

        ydl_opts = {
            'format': self.fmt,
            'cookiefile': str(self.cookiefile),
            'outtmpl': str(self.outtmpl),
            'logger': YtLogger(self.console_output),
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        self.console_output.emit("[Success] Download Complete")
