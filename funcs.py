from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ForceReply,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import os
from os import walk, remove

from pathlib import Path
from py7zr import SevenZipFile, FILTER_COPY
from multivolumefile import MultiVolume
from pyobidl.utils import sizeof_fmt
from ClientUpdate import DVUpload
from progress import progress_telegram, progress_pyobidl, progress_ytdlp


def sevenzip(fpath: Path, username, database, password: str = None, volume=None):
    ext = database[username]["ext"]
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name + f".{ext}"),
        mode="wb",
        volume=volume,
        ext_digits=ext_digits,
    ) as archive:
        with SevenZipFile(
            archive, "w", filters=filters, password=password
        ) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files


def limite_msg(text, message):
    lim_ch = 1500
    lines = text.splitlines()
    current_message = ""
    for line in lines:
        if len(current_message + "\n" + line) > lim_ch:
            message.reply(current_message)
            current_message = line
        else:
            current_message += "\n" + line

    if current_message:
        message.reply(current_message)


def get_file_size(file):
    file_size = os.stat(file)
    return file_size.st_size


def get_formats_youtube(url, username, msg, database):
    try:
        ydl = yt_dlp.YoutubeDL({})
        info = ydl.extract_info(url, download=False)
        formats = info["formats"]
        database[username]["title"] = info["title"]
        buttons = []
        for format in formats:
            button = InlineKeyboardButton(
                format["resolution"] + " " + format["ext"],
                callback_data="/yd " + format["format_id"],
            )
            if "acodec" in format:
                if format["acodec"] != "none":
                    buttons.append(button)
        keyboard = InlineKeyboardMarkup([[button] for button in buttons])
        msg.edit_text(
            f'__🔎Formatos disponibles__\n\n{info["title"]}', reply_markup=keyboard
        )
        return formats
    except Exception as ex:
        message.reply("__❌Error❌__\n\n" + str(ex))


def gme(file, msg, message, username, database):
    try:
        userdata = database[username]
        zips = userdata["zips"]
        file_size = get_file_size(file)
        parts = 1024 * 1024 * zips

        thumb = userdata["thumb"]
        caption = userdata["caption"]
        
        if caption == "":
            caption = None

        if not os.path.isfile(thumb):
            thumb = "thumb.png"

        user = userdata["user"]
        passw = userdata["passw"]
        host = userdata["host"]
        repo = userdata["repo"]
        
        DV = DVUpload(user,passw,host,repo=repo)
        is_login = DV.login()
        if file_size > parts:
            msg.edit_text("__✂️Dividiendo archivos " + str(sizeof_fmt(parts)) + "__")
            files = sevenzip(file, username, database, volume=parts)
            links = []
            a = 0
            for file in files:
                msg.edit_text(f"🔝Subiendo\n{file}\n{a}/{len(files)} partes")
                a += 1
                link = DV.upload(file)
                links.append(link)
                os.remove(file)
            txtname = os.path.split(file)[1] + ".txt"
            with open(txtname, "w") as t:
                n = ""
                links_msg = ""
                for li in links:
                    links_msg += "🔗" + li + "\n"
                    n += li + "\n"
                    t.write(n)
                t.close()
            n = f"__☁️Subida finalizada__\n\n{links_msg}"
            limite_msg(n, message)
            message.reply_document(txtname, thumb=thumb, caption=caption)
            database[username]["totalUpload"] += file_size
        else:
            link = DV.upload(file)
            txtname = os.path.split(file)[1] + ".txt"
            with open(txtname, "w") as t:
                t.write(link)
                t.close()
            n = f"__☁️Subida finalizada__\n\n🔗{link}"
            limite_msg(n, message)
            message.reply_document(txtname, thumb=thumb, caption=caption)
            database[username]["totalUpload"] += file_size
    except Exception as ex:
        message.reply("__❌Error❌__\n\n" + str(ex))


# Comprimir archivos
def compress(file, msg, message, username, database):
    try:
        userdata = database[username]
        zips = userdata["zips"]
        file_size = get_file_size(file)
        parts = 1024 * 1024 * zips

        thumb = userdata["thumb"]
        caption = userdata["caption"]

        if caption == "":
            caption = None

        if not os.path.isfile(thumb):
            thumb = "thumb.png"

        if file_size > parts:
            msg.edit_text("__✂️Dividiendo archivos " + str(sizeof_fmt(parts)) + "__")
            files = sevenzip(file, username, database, volume=parts)
            for file in files:
                message.reply_document(
                    file,
                    thumb=thumb,
                    caption=caption,
                    progress=progress_telegram,
                    progress_args=(msg, file),
                )
        else:
            message.reply_document(
                file,
                thumb=thumb,
                caption=caption,
                progress=progress_telegram,
                progress_args=(msg, file),
            )
    except Exception as ex:
        message.reply("__❌Error❌__\n\n" + str(ex))
