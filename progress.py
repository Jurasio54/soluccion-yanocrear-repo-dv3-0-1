import time
from time import time, localtime
import datetime
from pyobidl.utils import sizeof_fmt
from pyobidl.downloader import Downloader


def update_progress_bar(current, total):
    percentage = current / total
    percentage *= 100
    percentage = round(percentage)
    hashes = int(percentage / 5)
    spaces = 20 - hashes
    progress_bar = "[ " + "•" * hashes + "•" * spaces + " ]"
    percentage_pos = int(hashes / 1)
    percentage_string = str(percentage) + "%"
    progress_bar = (
        progress_bar[:percentage_pos]
        + percentage_string
        + progress_bar[percentage_pos + len(percentage_string) :]
    )
    return progress_bar


sec = 0


def progress_telegram(current, total, msg, file=""):
    global sec
    if sec != localtime().tm_sec:
        try:
            if file:
                text = "__📤Subiendo...\n\n__"
            else:
                text = "__📩Descargando__\n\n"
            text += f"__{update_progress_bar(current,total)}\n__"
            text += f"__📂Nombre: {file}\n\n__"
            text += f"__💯Progreso: {current * 100 / total:.1f}%\n__"
            text += f"__📄Tamańo: {sizeof_fmt(total)}\n__"
            text += f"__🗳Subido: {sizeof_fmt(current)}__"
            msg.edit_text(text)
        except:
            pass
    sec = localtime().tm_sec


def progress_pyobidl(
    dl: Downloader, file: str, index: int, total: int, speed: int, time: int, args
):
    msg = args[0]
    global sec
    if sec != localtime().tm_sec:
        try:
            text = "__📥Descargando...\n\n__"
            text += f"__📂Nombre: {file}\n\n__"
            text += f"__💯Progreso: {index * 100 / total:.1f}%\n__"
            text += f"__📄Tamańo: {sizeof_fmt(total)}\n__"
            text += f"__🗂️Descargado: {sizeof_fmt(index)}\n__"
            text += f"__⚡️Velocidad: {sizeof_fmt(speed)}__"
            msg.edit_text(text)
        except:
            pass
    sec = localtime().tm_sec


def progress_ytdlp(d, msg, file):
    if d["status"] == "downloading":
        global sec
        if sec != localtime().tm_sec:
            try:
                progress = d["_percent_str"]
                speed = d["_speed_str"]
                eta = d["_eta_str"]
                text = "__📥Descargando...__\n\n"
                text += f"__📂Nombre: {file}\n\n__"
                text += f"__💯Progreso: {progress}\n__"
                text += f"__⚡️Velocidad: {speed}\n__"
                text += f"__🕛Tiempo estimado: {eta}__"
                msg.edit_text(text)
            except:
                pass
        sec = localtime().tm_sec
