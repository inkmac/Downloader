import subprocess

from PySide6.QtCore import QThread, Signal


class FetchFormatWorker(QThread):
    result_ready = Signal(str)

    def __init__(
            self,
            url: str,
            cookie: str
    ):
        super().__init__()
        self.url = url
        self.cookie = cookie


    def run(self):
        self.echo_available_format(self.url, self.cookie)


    def echo_available_format(
            self,
            url: str,
            cookie: str
    ):
        command = [
            "yt-dlp.exe",
            "--cookies", cookie,
            "--verbose",
            "-F", url
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stdout.readline()
            if output:
                self.result_ready.emit(output.strip())
            if output == '' and process.poll() is not None:
                break

        return_code = process.poll()
        if return_code != 0:
            self.result_ready.emit(f"输出可用视频格式 命令执行失败，错误: {process.stderr.read()}")
            return