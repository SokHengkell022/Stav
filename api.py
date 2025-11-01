from . import sessions
import re
import logging
import os
import json as jsonlib
log_file_path = os.path.expanduser("~/.stav_log.txt")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
def log_request(method, url, **kwargs):
    """Mencatat semua request (metode, URL, payload)."""
    log_data = {
        "method": method.upper(),
        "url": url,
        "params": kwargs.get("params"),
        "data": kwargs.get("data"),
        "json": kwargs.get("json"),
        "headers": kwargs.get("headers"),
    }
    log_data = {k: v for k, v in log_data.items() if v is not None}
    logging.info(f"REQUEST: {jsonlib.dumps(log_data, ensure_ascii=False)}")
def log_blocked_access(url):
    """Mencatat akses URL yang diblokir."""
    logging.warning(f"Akses ke URL diblokir: {url}")
def is_url_blocked(url):
    """Memeriksa apakah URL termasuk dalam daftar blokir."""
    blocked_url_patterns = [
        r"(telegram\.me|t\.me|api\.telegram\.org)",
        r"(discord\.gg|discordapp\.com|discord\.com)"
    ]
    return any(re.search(pattern, url, re.IGNORECASE) for pattern in blocked_url_patterns)
def request(method, url, **kwargs):
    """Membuat dan mengirimkan objek :class:`Request <Request>`."""
    log_request(method, url, **kwargs)
    if is_url_blocked(url):
        log_blocked_access(url)
        raise ValueError(f"Akses ke URL ({url}) telah diblokir oleh STAV.")
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)
def get(url, params=None, **kwargs):
    r"""Mengirimkan permintaan GET."""
    print(f"STAV: Mencoba mengakses URL (GET): {url}")
    return request("get", url, params=params, **kwargs)
def options(url, **kwargs):
    r"""Mengirimkan permintaan OPTIONS."""
    return request("options", url, **kwargs)
def head(url, **kwargs):
    r"""Mengirimkan permintaan HEAD."""
    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)
def post(url, data=None, json=None, **kwargs):
    r"""Mengirimkan permintaan POST."""
    print(f"STAV: Mencoba mengakses URL (POST): {url}")
    return request("post", url, data=data, json=json, **kwargs)
def put(url, data=None, **kwargs):
    r"""Mengirimkan permintaan PUT."""
    return request("put", url, data=data, **kwargs)
def patch(url, data=None, **kwargs):
    r"""Mengirimkan permintaan PATCH."""
    return request("patch", url, data=data, **kwargs)
def delete(url, **kwargs):
    r"""Mengirimkan permintaan DELETE."""
    return request("delete", url, **kwargs)
