import json
from .logging import get_logger

_log = get_logger()

# 定义 user.json 读写函数

def load_users():
    try:
        with open("user.json", "r", encoding="utf-8") as f:
            return json.load(f)
        _log.info("load user.json success")
    except (FileNotFoundError, json.JSONDecodeError):
        _log.warning("user.json not found or decode error")
        return {}

def save_users(users):
    with open("user.json", "w", encoding="utf-8") as f:
        _log.info("save user.json success")
        json.dump(users, f, ensure_ascii=False, indent=4)
