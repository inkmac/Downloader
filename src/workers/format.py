import traceback

from PySide6.QtCore import QThread, Signal
from tabulate import tabulate
from yt_dlp import YoutubeDL

from src.utils.logger import YtLogger


class FetchFormatWorker(QThread):
    console_output = Signal(str)
    video_formats_ready = Signal(list)
    audio_formats_ready = Signal(list)

    def __init__(
            self,
            url: str,
            cookie: str
    ):
        super().__init__()
        self.url = url
        self.cookie = cookie


    def run(self):
        try:
            self.download()
        except Exception as e:
            self.console_output.emit(f"[Exception] 获取格式失败: {str(e)}")
            traceback.print_exc()


    def download(self):
        ydl_opts = {
            'cookiefile': self.cookie,
            'logger': YtLogger(self.console_output),
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)

        formats = info.get('formats', [])
        if not formats:
            self.console_output.emit("未能获取到可用格式信息。")
            return

        headers: list[str] = ["ID", "EXT", "RESOLUTION", "FILESIZE"]
        rows: list[list[str]] = []

        video_format_ids: list[str] = []
        audio_format_ids: list[str] = []

        for f in formats:
            if f.get('ext') == 'mhtml':
                continue

            fmt_id = f.get('format_id')
            ext = f.get('ext') or 'N/A'
            res = f.get('resolution') or f"{f.get('width', '?')}x{f.get('height', '?')}" or 'audio only'

            filesize = f.get('filesize')
            filesize_str = f"{filesize / (1024 * 1024):.2f}MiB" if filesize else 'N/A'

            rows.append([fmt_id, ext, res, filesize_str])

            if f.get('vcodec', 'none') != 'none':
                video_format_ids.append(fmt_id)
            elif f.get('acodec', 'none') != 'none':
                audio_format_ids.append(fmt_id)

        table_str = tabulate(rows, headers=headers, tablefmt="plain")
        divider = '-' * len(table_str.splitlines()[0])

        # send format table
        self.console_output.emit(divider)
        self.console_output.emit(table_str)
        self.console_output.emit(divider)
        self.console_output.emit("可用格式已更新，可以在『视频格式』下拉框中选择想要下载的格式 ID")

        # send format id signal
        self.video_formats_ready.emit(video_format_ids)
        self.audio_formats_ready.emit(audio_format_ids)