import traceback

from PySide6.QtCore import QThread, Signal
from tabulate import tabulate
from yt_dlp import YoutubeDL

from src.utils.logger import YtLogger


class FetchFormatWorker(QThread):
    console_output = Signal(str)

    def __init__(
            self,
            url: str,
            cookie: str
    ):
        super().__init__()
        self.url = url
        self.cookie = cookie


    def run(self):
        ydl_opts = {
            'cookiefile': self.cookie,
            'logger': YtLogger(self.console_output),
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                formats = info.get('formats', [])
                if not formats:
                    self.console_output.emit("未能获取到可用格式信息。")
                    return

                headers = ["ID", "EXT", "RESOLUTION", "FILESIZE"]
                rows = []

                for f in formats:
                    fmt_id = f.get('format_id') or 'N/A'
                    ext = f.get('ext') or 'N/A'
                    res = f.get('resolution') or f"{f.get('width', '?')}x{f.get('height', '?')}" or 'audio only'

                    filesize = f.get('filesize')
                    filesize_str = f"{filesize / (1024 * 1024):.2f}MiB" if filesize else 'N/A'

                    rows.append([fmt_id, ext, res, filesize_str])

                table_str = tabulate(rows, headers=headers, tablefmt="plain")
                self.console_output.emit(table_str)

        except Exception as e:
            self.console_output.emit(f"[Exception] 获取格式失败: {str(e)}")
            traceback.print_exc()