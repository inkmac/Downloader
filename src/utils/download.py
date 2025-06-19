import subprocess
import time

from PySide6.QtCore import QThread, Signal


class DownloadWorker(QThread):
    result_ready = Signal(str)

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
        self.download_video(self.url, self.cookie, self.fmt, self.output)


    def download_video(
            self,
            url: str,
            cookie: str,
            fmt: str,
            output: str
    ) -> tuple[float, float]:

        command = [
            "yt-dlp.exe",
            "--cookies", cookie,
            "-f", fmt,
            "-o", output,
            url
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        download_start_time: float = time.time()
        merge_start_time: float = -1

        download_time: float = 0

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if '[download]' in output and 'has already been downloaded' in output:
                    self.result_ready.emit(output.strip())
                    return -1, -1

                # will reach if no exception or already downloaded
                if '[Merger] Merging formats into' in output:
                    download_time = time.time() - download_start_time
                    self.result_ready.emit(f'视频下载耗时 {download_time:.2f} 秒')
                    merge_start_time = time.time()

                self.result_ready.emit(output.strip())

        return_code = process.poll()
        if return_code != 0:
            raise Exception(f"命令执行失败，错误: {process.stderr.read()}")

        merge_time = time.time() - merge_start_time
        self.result_ready.emit(f'视频合并耗时 {merge_time:.2f} 秒')

        return download_time, merge_time