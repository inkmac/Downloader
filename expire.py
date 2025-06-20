import json
import sys
import winreg
from datetime import datetime, timedelta
from typing import TypedDict

from cryptography.fernet import Fernet

REG_PATH = r'Software\MyApp1'
REG_NAME = 'date_config'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

SECRET_KEY = b'6TymdYXbZq9GO3F1RMz4aOt8mW0zGyeTIHuogmKsVzE='
fernet = Fernet(SECRET_KEY)


class RegConfig(TypedDict):
    first_used_time: str
    expire_day: int
    expire_date_time: str
    latest_used_time: str
    is_expired: bool


def get_current_time() -> datetime:
    return datetime.now()


def format_date_time(date_time: datetime) -> str:
    return date_time.strftime(DATETIME_FORMAT)


def parse_date_time(date_time: str) -> datetime:
    return datetime.strptime(date_time, DATETIME_FORMAT)


def read_register() -> RegConfig | None:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH) as reg_key:
            value, _ = winreg.QueryValueEx(reg_key, REG_NAME)

        decrypted = fernet.decrypt(value.encode())
        return json.loads(decrypted.decode())
    except FileNotFoundError:
        return None
    except:
        sys.exit(1)


def write_register(data: RegConfig):
    try:
        bytes_data = json.dumps(data).encode()
        encrypted = fernet.encrypt(bytes_data).decode()

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH) as reg_key:
            winreg.SetValueEx(reg_key, REG_NAME, 0, winreg.REG_SZ, encrypted)
    except:
        sys.exit(1)


def is_config_initialized() -> bool:
    return read_register() is not None


def initialize_config(expire_day: int = 30):
    if is_config_initialized():
        return

    first_used_time = get_current_time()
    expire_date_time = get_current_time() + timedelta(days=expire_day)
    data: RegConfig = {
        'first_used_time': format_date_time(first_used_time),
        'expire_day': expire_day,
        'expire_date_time': format_date_time(expire_date_time),
        'latest_used_time': format_date_time(first_used_time),
        'is_expired': False
    }
    write_register(data)


def save_current_time(current_time: datetime):
    data = read_register()

    latest_used_time: datetime = parse_date_time(data['latest_used_time'])
    expire_date_time: datetime = parse_date_time(data['expire_date_time'])

    # 检查时间是否异常, 系统时间是否被修改提前
    # 如果异常, 直接设置为expired
    if current_time < latest_used_time:
        data['is_expired'] = True

    # 检测当前时间是否过期
    if current_time > expire_date_time:
        data['is_expired'] = True

    data['latest_used_time'] = format_date_time(current_time)

    write_register(data)


def is_expired() -> bool:
    data = read_register()

    is_expire: bool = data['is_expired']
    if is_expire:
        return True

    return False


__all__ = ['initialize_config', 'save_current_time', 'is_expired']