import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

COOKIES_DIR = BASE_DIR / 'cookies'
VIDEOS_DIR = BASE_DIR / 'videos'