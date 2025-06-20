import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

COOKIES_DIR = BASE_DIR / 'cookies'
VIDEOS_DIR = BASE_DIR / 'videos'
DOWNLOAD_CONFIGS_PATH = BASE_DIR / 'config' / 'download_config.json'

SITE_CONFIGS = {
    'bilibili.com': {
        'label': 'bilibili',
        'cookie': COOKIES_DIR / 'bilibili.com_cookies.txt',
        'output': VIDEOS_DIR / 'bilibili' / '%(title)s.%(ext)s',
    },
    'youtube.com': {
        'label': 'YouTube',
        'cookie': COOKIES_DIR / 'youtube.com_cookies.txt',
        'output': VIDEOS_DIR / 'youtube' / '%(title)s.%(ext)s',
    }
}