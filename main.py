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

import time
from time import time, localtime
import datetime

import shutil
from shutil import rmtree

import zipfile
from zipfile import ZipFile

import infos

from bs4 import BeautifulSoup
import requests, sys
from requests import get
from user_agent import generate_user_agent

import yt_dlp
from PIL import Image
import psutil

from pyobidl.downloader import Downloader
from pyobidl.utils import sizeof_fmt

from progress import progress_telegram, progress_pyobidl, progress_ytdlp
from bs4 import BeautifulSoup

import asyncio

from ClientUpdate import DVUpload
import threading

from funcs import gme, get_formats_youtube, sevenzip, compress


app = Client(
    "bot",
    api_id="12729863",
    api_hash="ebb09446c3def9fc6c69f1a10e1252a0",
    bot_token="6659987824:AAHkXFMVJGr-UgLBf-bcfPzI6A1_Wy4COtA",
)

database = {
    "diago8888": {
        "zips": 4,
        "old_name": "",
        "admin": True,
        "yt": "",
        "title": "",
        "thumb": "",
        "caption": "",
        "files": [],
        "autoup": False,
        "host": "",
        "user": "",
        "passw": "",
        "repo": "",
        "proxy": "",
        "ext": "zip",
        "mode": "US",
        "totalUpload": 0,
    },
    "demian2008": {
        "zips": 4,
        "old_name": "",
        "admin": True,
        "yt": "",
        "title": "",
        "thumb": "",
        "caption": "",
        "files": [],
        "autoup": False,
        "host": "",
        "user": "",
        "passw": "",
        "repo": "",
        "proxy": "",
        "ext": "zip",
        "mode": "US",
        "totalUpload": 0,
    },
}

nubes = [
    {
        "user": "yuca1",
        "passw": "Yuca23*12",
        "host": "https://revfhs.sld.cu/index.php/fhs/",
        "repo": 536,
        "zips": 15,
    },
    {
        "user": "diago",
        "passw": "Diagogoogle$4",
        "host": "https://revmediciego.sld.cu/index.php/mediciego/",
        "repo": 530,
        "zips": 2,
    },
]


def select_type(file, message, username):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✈️TELEGRAM", callback_data="/telegram")],
            [InlineKeyboardButton("☁️NUBE", callback_data="/gme")],
        ]
    )
    message.reply("__👌Elige el tipo de subida__", reply_markup=buttons)


@app.on_callback_query()
def callbackquery(app, callback_query):

    message = callback_query.message
    username = callback_query.from_user.username
    id = callback_query.from_user.id

    root = f"./downloads/{username}/"

    data = callback_query.data

    if username in database:

        if data == "/bot_data":
            disk = psutil.disk_usage("/")
            ram = psutil.virtual_memory()
            users_count = len(database)
            users = []
            for user in database:
                users.append(user)
            totalUpload = database[username]["totalUpload"]
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/atras")]]
            )
            message.edit_text(
                infos.status(disk, ram, users_count, users, totalUpload),
                reply_markup=buttons,
            )

        if data == "/change_cloud":
            a = -1
            button_list = []
            msg = "**🌩️Nubes disponibles\n\n**"
            for nube in nubes:
                a += 1
                user = nube["user"]
                passw = nube["passw"]
                host = nube["host"]
                repo = nube["repo"]
                zips = nube["zips"]
                msg += f"**Nube{str(a)} - {host}\n**"
                msg += f"**User: {user} | Passw: {passw}\n**"
                msg += f"**Repo: {str(repo)} | Zips: {str(zips)}\n\n**"
                button_list.append(
                    [
                        InlineKeyboardButton(
                            "🌩️Nube" + str(a), callback_data="/nube " + str(a)
                        ),
                        InlineKeyboardButton("🗑️", callback_data="/del_cloud " + str(a)),
                    ]
                )
            button_list.append(
                [InlineKeyboardButton("🔙Atrás🔙", callback_data="/atras")]
            )  # Añade el botón "Atrás" al final
            buttons = InlineKeyboardMarkup(
                button_list
            )  # Crea el teclado con todas las filas
            msg += "\n\n⛔Att: Esto cambia la nube a todos los usuarios del bot"
            message.edit_text(msg, reply_markup=buttons)

        if "nube" in data:
            split = int(data.split(" ")[1])
            for user in database:
                database[user]["user"] = nubes[split]["user"]
                database[user]["passw"] = nubes[split]["passw"]
                database[user]["host"] = nubes[split]["host"]
                database[user]["repo"] = nubes[split]["repo"]
                database[user]["zips"] = nubes[split]["zips"]
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/atras")]]
            )
            message.edit_text("🌩️Nube cambiada", reply_markup=buttons)

        if "/del_cloud" in data:
            ind = int(data.split(" ")[1])
            del nubes[ind]
            a = -1
            button_list = []
            msg = "**🌩️Nubes disponibles\n\n**"
            for nube in nubes:
                a += 1
                user = nube["user"]
                passw = nube["passw"]
                host = nube["host"]
                repo = nube["repo"]
                zips = nube["zips"]
                msg += f"**Nube{str(a)} - {host}\n**"
                msg += f"**User: {user} | Passw: {passw}\n**"
                msg += f"**Repo: {str(repo)} | Zips: {str(zips)}\n\n**"
                button_list.append(
                    [
                        InlineKeyboardButton(
                            "🌩️Nube" + str(a), callback_data="/nube" + str(a)
                        ),
                        InlineKeyboardButton("🗑️", callback_data="/del_cloud " + str(a)),
                    ]
                )
            button_list.append(
                [InlineKeyboardButton("🔙Atrás🔙", callback_data="/atras")]
            )  # Añade el botón "Atrás" al final
            buttons = InlineKeyboardMarkup(
                button_list
            )  # Crea el teclado con todas las filas
            msg += "\n\n⛔Att: Esto cambia la nube a todos los usuarios del bot"
            message.edit_text(msg, reply_markup=buttons, disable_web_page_preview=True)

        if data == "/mydata":
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/atras")]]
            )
            message.edit_text(
                infos.config(username, database),
                reply_markup=buttons,
                disable_web_page_preview=True,
            )
        if data == "/up_all":
            files = os.listdir(root)
            for file in files:
                msg = message.reply("__📪Preparando...__")
                compress(root + file, msg, message, username)
                msg.edit_text("__📤Subida finalizada__")

        if data == "/atras":
            if database[username]["admin"]:
                buttons = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📄Archivos", callback_data="/files"),
                            InlineKeyboardButton("⚙️Datos", callback_data="/mydata"),
                        ],
                        [
                            InlineKeyboardButton(
                                "📉Bot (Datos)", callback_data="/bot_data"
                            ),
                            InlineKeyboardButton(
                                "🌩️Nube (Cambiar)", callback_data="/change_cloud"
                            ),
                        ],
                    ]
                )
            else:
                buttons = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("📄Archivos", callback_data="/files")],
                        [InlineKeyboardButton("⚙️Datos", callback_data="/mydata")],
                    ]
                )
            msg_start = infos.start()
            message.edit_text(msg_start, reply_markup=buttons)

        if data == "/options":
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🌃Thumb", callback_data="/thumb"),
                        InlineKeyboardButton("📝Caption", callback_data="/caption"),
                    ],
                    [
                        InlineKeyboardButton("🔁Default", callback_data="/default"),
                        InlineKeyboardButton("📚Ext", callback_data="/ext"),
                    ],
                    [InlineKeyboardButton("🔙Atrás🔙", callback_data="/files")],
                ]
            )
            message.edit_text(infos.options(), reply_markup=buttons)

        if data == "/thumb":
            message.edit_text("🏙️Envía una foto", reply_markup=ForceReply())

        if data == "/caption":
            message.edit_text("📝Envía una descripción", reply_markup=ForceReply())

        if data == "/default":
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/options")]]
            )
            database[username]["thumb"] = ""
            database[username]["caption"] = ""
            message.edit_text("__👌Listo__", reply_markup=buttons)

        if data == "/ext":
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📚zip", callback_data="/ext_zip"),
                        InlineKeyboardButton("📚7z", callback_data="/ext_7z"),
                    ],
                    [InlineKeyboardButton("🔙Atrás🔙", callback_data="/options")],
                ]
            )
            message.edit_text(
                "📚Elige la extensión de los archivos", reply_markup=buttons
            )

        if data == "/ext_7z":
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/options")]]
            )
            database[username]["ext"] = "7z"
            message.edit_text("__📚Extensión cambiada a .7z__", reply_markup=buttons)

        if data == "/ext_zip":
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/options")]]
            )
            database[username]["ext"] = "zip"
            message.edit_text("__📚Extensión cambiada a .zip__", reply_markup=buttons)

        if data == "/delall":
            rmtree(root)
            os.mkdir(root)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/files")]]
            )
            message.edit_text("__🗑Eliminado🗑️__", reply_markup=buttons)

        if "/yd" in data:
            try:
                url = database[username]["yt"]
                format_id = data.split(" ")[1]
                msg = message.edit_text("__📥Descargando...__")
                file = database[username]["title"]
                ydl_opts = {
                    "format": format_id,
                    "outtmpl": root + "%(title)s.%(ext)s",
                    "progress_hooks": [lambda d: progress_ytdlp(d, msg, file)],
                }
                ydl = yt_dlp.YoutubeDL(ydl_opts)
                ydl.download([url])
                file = file + ".mp4"
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📄Archivos", callback_data="/files")]]
                )
                msg.edit_text("__📥Descarga finalizada__", reply_markup=buttons)
                # compress(file,msg,message,username)
            except Exception as ex:
                msg.edit_text("__❌Error❌__\n\n" + str(ex))

        if data == "/autoup":
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("✅Encender", callback_data="/autoup_on"),
                        InlineKeyboardButton("☑️Apagar", callback_data="/autoup_off"),
                    ],
                    [InlineKeyboardButton("🔙Atrás🔙", callback_data="/options")],
                ]
            )
            message.edit_text(
                "__⚡️Subidas automática\n\n👌Activa o desactiva la subida automática__",
                reply_markup=buttons,
            )

        if data == "/autoup_on":
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/files")]]
            )
            database[username]["autoup"] = True
            message.edit_text("__✅Subida automática activada__", reply_markup=buttons)

        if data == "/autoup_off":
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/files")]]
            )
            database[username]["autoup"] = False
            message.edit_text(
                "__☑️️Subida automática desactivada__", reply_markup=buttons
            )

        if data == "/gme":
            file = database[username]["old_name"]
            msg = message.edit_text("__Preparando...__")
            gme(file, msg, message, username, database)

        if data == "/telegram":
            file = database[username]["old_name"]
            msg = message.edit_text("__📤Subiendo...__")
            compress(file, msg, message, username, database)
            msg.edit_text("__📤Subida finalizada__")

        if data == "/files":
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⚡️AutoUp", callback_data="/autoup"),
                        InlineKeyboardButton("☁️Subir", callback_data="/up_all"),
                    ],
                    [
                        InlineKeyboardButton("🗑Eliminar️️", callback_data="/delall"),
                        InlineKeyboardButton("📪Opciones", callback_data="/options"),
                    ],
                    [InlineKeyboardButton("🔙Atrás🔙", callback_data="/atras")],
                ]
            )
            message.edit_text(infos.files(root), reply_markup=buttons)


@app.on_message(filters.reply)
def Reply(app, message):

    text = message.text
    username = message.from_user.username
    id = message.from_user.id
    root = f"./downloads/{username}/"
    thumb = f"./thumbs/{username}/"
    thumb_img = f"./thumbs/{username}/thumb.png"

    if not os.path.exists(thumb):
        os.makedirs(thumb)

    data = message.reply_to_message.text

    if data == "🏙️Envía una foto":
        try:
            app.download_media(message, thumb_img)
            original_image = Image.open(thumb_img)
            resized_image = original_image.resize((320, 320))
            resized_image.save(thumb_img)
            database[username]["thumb"] = thumb_img
            message.reply("__🏙️Imagen guardada__")
        except:
            message.reply("🏙️Envía una imagen")

    if data == "📝Envía una descripción":
        caption = text
        database[username]["caption"] = caption
        message.reply("📝Descripción guardada")

    if data == "✍️Ingresa el nuevo nombre del archivo":
        new_name = text
        old_name = database[username]["old_name"]
        os.rename(old_name, root + new_name)
        message.reply("__✍️Renombrado__")

    if data == "✍️Ingresa el nuevo nombre de la carpeta":
        new_name = text
        old_name = database[username]["old_name"]
        os.rename(old_name, root + new_name)
        message.reply("__✍️Renombrado__")

    if data == "🔐Escribe una contraseńa para tus archivos":
        database[username]["z_passw"] == text
        message.reply("__🔐Contraseńa guardada__")


def download(app, username, msg):
    root = f"./downloads/{username}/"
    file_name = root
    files = database[username]["files"]
    for file in files:
        app.download_media(
            file, file_name, progress=progress_telegram, progress_args=(msg,)
        )
    database[username]["files"] = []


# Detectar archivos y descargar
@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
def detect_file(client, message):

    username = message.from_user.username
    root = f"./downloads/{username}/"
    user = database[username]["user"]
    passw = database[username]["passw"]
    host = database[username]["host"]
    repo = database[username]["repo"]
    
    try:
        filename = message.document.file_name
        if filename.split(".")[-1] == "txt":
            txt = message.download(file_name="./")
            archivo = open(txt, "r")
            msg = message.reply("__🗑️Eliminando__")
            for url in archivo.readlines():
                url = url.split("\n")[0]
            msg.edit_text("__🗑Enlaces eliminados__")
            archivo.close()
        else:
            database[username]["files"].append(message)
            buttons = ReplyKeyboardMarkup(
                [["📥Descargar"], ["🚫Cancelar"]], resize_keyboard=True
            )
            msg = message.reply("__📪️Archivo cargado...__", reply_markup=buttons)
    except:
        database[username]["files"].append(message)
        buttons = ReplyKeyboardMarkup(
            [["📥Descargar"], ["🚫Cancelar"]], resize_keyboard=True
        )
        msg = message.reply("__📪️Archivo cargado...__", reply_markup=buttons)


####Comandos####
@app.on_message()
def commands(client, message):

    text = message.text
    username = message.from_user.username
    id = message.from_user.id
    root = f"./downloads/{username}/"

    if not os.path.exists(root):
        os.makedirs(root)

    if username in database:

        if "/start" in text:
            buttons_rows = [
                [InlineKeyboardButton("📄Archivos", callback_data="/files")],
                [InlineKeyboardButton("⚙️Datos", callback_data="/mydata")],
            ]
            if database[username]["admin"]:
                buttons_rows.append([
                    InlineKeyboardButton("📉Bot (Datos)", callback_data="/bot_data"),
                    InlineKeyboardButton("🌩️Nube (Cambiar)", callback_data="/change_cloud"),
                ])
            buttons = InlineKeyboardMarkup(buttons_rows)
            msg_start = infos.start()
            message.reply(msg_start, reply_markup=buttons)

        elif "📥Descargar" in text:
            msg = message.reply("__📥Descargando...__")
            download(app, username, msg)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("📄Archivos", callback_data="/files")]]
            )
            msg.edit_text("__📥Descarga finalizada__", reply_markup=buttons)

        elif "🚫Cancelar" in text:
            database[username]["files"] = []
            message.reply("__🚫Cancelado__")

        elif "/mk" in text:
            try:
                folder = text.split(" ")[1]
                path = os.path.join(root, folder)
                os.mkdir(path)
                message.reply("__📁Carpeta creada__")
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/dirrn" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                file = root + subdirs[split]
                database[username]["old_name"] = file
                message.reply(
                    "✍️Ingresa el nuevo nombre de la carpeta", reply_markup=ForceReply()
                )
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/thumb" in text:
            message.reply("🏙️Envía una foto", reply_markup=ForceReply())

        elif "/caption" in text:
            message.reply("📝Envía una descripción", reply_markup=ForceReply())

        elif "/dirdel" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                folder = root + subdirs[split]
                rmtree(folder)
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📄Archivos", callback_data="/files")]]
                )
                message.reply("__🗑Eliminado🗑__", reply_markup=buttons)
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/dirup" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                folder = root + subdirs[split]
                msg = message.reply("__📦Compriendo__")
                file = shutil.make_archive(folder, "zip", folder)
                msg.edit_text("__📪Preparando...__")
                compress(file, msg, message, username)
                msg.edit_text("__📤️Subida finalizada__")
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/copy" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                split2 = int(text.split("_")[2])
                file = root + files[split]
                folder = root + subdirs[split2]
                shutil.copy(file, folder)
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📄Archivos", callback_data="/files")]]
                )
                message.reply("__📄Copiado__", reply_markup=buttons)
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/move" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                split2 = int(text.split("_")[2])
                file = root + files[split]
                folder = root + subdirs[split2]
                shutil.move(file, folder)
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📄Archivos", callback_data="/files")]]
                )
                message.reply("__✂️Movido__", reply_markup=buttons)
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/add_user" in text:
            if database[username]["admin"] == True:
                user = text.split(" ")[1]
                database[user] = {
                    "zips": 100,
                    "old_name": "",
                    "admin": False,
                    "yt": "",
                    "title": "",
                    "thumb": "",
                    "caption": "",
                    "files": [],
                    "autoup": False,
                    "host": "",
                    "user": "",
                    "passw": "",
                    "repo": "",
                    "proxy": "",
                    "ext": "zip",
                    "mode": "US",
                    "totalUpload": 0,
                }
                message.reply(f"__👥Usuario agregado:\n@{user}__")
            else:
                message.reply("__❌Comando solo para admin❌__")

        elif "/add_admin" in text:
            if database[username]["admin"] == True:
                user = text.split(" ")[1]
                database[user] = {
                    "zips": 100,
                    "old_name": "",
                    "admin": True,
                    "yt": "",
                    "title": "",
                    "thumb": "",
                    "caption": "",
                    "files": [],
                    "autoup": False,
                    "host": "",
                    "user": "",
                    "passw": "",
                    "repo": "",
                    "proxy": "",
                    "ext": "zip",
                    "totalUpload": 0,
                }
                message.reply(f"__🔱Admin agregado\n@{user}__")
            else:
                message.reply(
                    "__❌Comando solo para admin❌__", reply_markup=buttons_support
                )

        elif "/ban_user" in text:
            user = text.split(" ")[1]
            del database[user]
            message.reply(f"❌@{user} baneado❌")

        elif "/zips" in text:
            size = int(text.split(" ")[1])
            database[username]["zips"] = size
            message.reply("__🗳️Zips configurados__")

        elif "/acc" in text:
            user = text.split(" ")[1]
            passw = text.split(" ")[2]
            database[username]["user"] = user
            database[username]["passw"] = passw
            message.reply("__👌Listo__")

        elif "/set_account" in text:
            if database[username]["admin"]:
                user = text.split(" ")[1]
                passw = text.split(" ")[2]
                for user in database:
                    if not database[user]["admin"]:
                        database[user]["user"] = user
                        database[user]["passw"] = passw
                message.reply("__👌Listo__")

        elif "/add_cloud" in text:
            if database[username]["admin"]:
                user = text.split(" ")[1]
                passw = text.split(" ")[2]
                host = text.split(" ")[3]
                repo = text.split(" ")[4]
                zips = text.split(" ")[5]
                nube = {
                    "user": user,
                    "passw": passw,
                    "host": host,
                    "repo": repo,
                    "zips": zips,
                }
                nubes.append(nube)
                message.reply("🌩️Nube agregada")

        elif "/del_cloud" in text:
            if database[username]["admin"]:
                ind = int(text.split(" ")[1])
                del nube[ind]
                message.reply("🗑️Nube eliminada")

        elif "/host" in text:
            host = text.split(" ")[1]
            database[username]["host"] = host
            message.reply("__👌Listo__")

        elif "/repo" in text:
            repo = int(text.split(" ")[1])
            database[username]["repo"] = repo
            message.reply("__👌Listo__")

        elif "/mydata" in text:
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/atras")]]
            )
            message.reply(
                infos.config(username, database),
                reply_markup=buttons,
                disable_web_page_preview=True,
            )

        elif "/options" in text:
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🌃Thumb", callback_data="/thumb"),
                        InlineKeyboardButton("📝Caption", callback_data="/caption"),
                    ],
                    [
                        InlineKeyboardButton("🔁Default", callback_data="/default"),
                        InlineKeyboardButton("📚Ext", callback_data="/ext"),
                    ],
                    [InlineKeyboardButton("🔙Atrás🔙", callback_data="/files")],
                ]
            )
            message.reply(infos.options(), reply_markup=buttons)
            
        elif "/makerepo" in text:
            try:
                user = database[username]["user"]
                passw = database[username]["passw"]
                host = database[username]["host"]
                DV = DVUpload(user,passw,host)
                DV.login()
                repo = DV.make_repo()
                message.reply(f"Repo creado {str(repo)}")
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))
                
        elif "/files" in text:
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⚡️AutoUp", callback_data="/autoup"),
                        InlineKeyboardButton("☁️Subir", callback_data="/up_all"),
                    ],
                    [
                        InlineKeyboardButton("🗑Eliminar️️", callback_data="/delall"),
                        InlineKeyboardButton("📪Opciones", callback_data="/options"),
                    ],
                    [InlineKeyboardButton("🔙Atrás🔙", callback_data="/atras")],
                ]
            )
            message.reply(infos.files(root), reply_markup=buttons)

        elif "/delall" in text:
            rmtree(root)
            os.mkdir(root)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙Atrás🔙", callback_data="/files")]]
            )
            message.reply("__🗑Eliminado__", reply_markup=buttons)

        elif "/del" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                file = root + files[split]
                os.remove(file)
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📄Archivos", callback_data="/files")]]
                )
                message.reply("__🗑Eliminado🗑__", reply_markup=buttons)
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/up_all" in text:
            files = os.listdir(root)
            for file in files:
                msg = message.reply("__📪Preparando...__")
                compress(root + file, msg, message, username, database)
                msg.edit_text("__📤Subida finalizada__")

        elif "/up" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                file = root + files[split]
                database[username]["old_name"] = file
                select_type(file, message, username)
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/sv" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                file = root + files[split]
                parts = database[username]["zips"] * 1024 * 1024
                msg = message.reply(
                    "__✂️Dividiendo archivos " + str(sizeof_fmt(parts)) + "__"
                )
                sevenzip(file, username, database, volume=parts)
                msg.edit_text("__👌Comprimido__")
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "/rn" in text:
            try:
                dir, subdirs, files = next(walk(root))
                split = int(text.split("_")[1])
                file = root + files[split]
                database[username]["old_name"] = file
                message.reply(
                    "✍️Ingresa el nuevo nombre del archivo", reply_markup=ForceReply()
                )
            except Exception as ex:
                message.reply("__❌Error❌__\n\n" + str(ex))

        elif "youtube.com" in text or "youtu.be" in text or "twitch" in text:
            database[username]["yt"] = text
            msg = message.reply("__🔗Obteniendo formatos__")
            formats = get_formats_youtube(text, username, msg, database)

        elif "http" in text:
            url = text
            msg = message.reply("__📥Descargando...__")
            dl = Downloader(destpath=root)
            file = dl.download_url(
                url=text, progressfunc=progress_pyobidl, args=(msg, app)
            )
            if file != None:
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📄Archivos", callback_data="/files")]]
                )
                msg.edit_text("__📥Descarga finalizada__", reply_markup=buttons)
                if database[username]["autoup"] == True:
                    compress(file, msg, message, username, database)
                    msg.edit_text("__📤Subida finalizada__")
            else:
                msg.edit_text("__🔗Error en el link__")

    else:
        message.reply("__🚫No tiene acceso🚫\n\n📝Contactar: @diago8888__")


print("👾Bot Online👾")
app.run()