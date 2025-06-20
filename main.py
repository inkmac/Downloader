import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication

import expire
from src.downloader import Downloader


def main():
    expire.initialize_config()

    if expire.is_expired():
        sys.exit(1)

    expire.save_current_time(datetime.now())

    app = QApplication([])
    window = Downloader()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()