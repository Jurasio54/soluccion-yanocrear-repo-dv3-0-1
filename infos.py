import os
from os import walk

##from pyobidl.utils import sizeof_fmt


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (round(num), unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Y", suffix)


def files(root):
    listado = os.listdir(root)
    dir, subdirs, files = next(walk(root))
    sms = "**——>Files:<——\n\n**"
    sn = -1
    for s in subdirs:
        sn += 1
        if len(s) > 20:
            sms += f"**{s[:20]}...\n**"
        else:
            sms += f"**{s}\n**"
        sms += f"**———> /dirup_{sn}\n**"
        sms += f"**——> /dirrn_{sn}\n**"
        sms += f"**—> /dirdel_{sn}\n\n**"
    an = -1
    for a in files:
        an += 1
        size = (a, os.stat(os.path.join(root, a)).st_size)
        size = size[1]
        if len(a) > 20:
            sms += f"**{a[:20]}... - {str(sizeof_fmt(size))}\n**"
        else:
            sms += f"**{a} - {str(sizeof_fmt(size))}\n**"
        sms += f"**———> /up_{an}\n**"
        sms += f"**——> /rn_{an}\n**"
        sms += f"**—> /del_{an}\n\n**"
    return sms


def config(username, database):
    msg = "**•Id: @" + str(username) + "\n\n**"
    msg += "**——>Nube<——**\n"
    msg += "**•User: " + str(database[username]["user"]) + "**\n"
    msg += "**•Passw: " + str(database[username]["passw"]) + "**\n"
    msg += "**•Host: " + str(database[username]["host"]) + "**\n\n"
    msg += "**——>Otros<——**\n"
    msg += "**•Repo: " + str(database[username]["repo"]) + "**\n"
    msg += "**•Zips: " + str(database[username]["zips"]) + "MB**\n"
    msg += "**️•Proxy: " + str(database[username]["proxy"]) + "**\n"
    if database[username]["admin"]:
        msg += "**•Rol: Admin**"
    else:
        msg += "**•Rol: User**"
    return msg


def start():
    msg = "__⚡️DV-Company__\n\n"
    msg += "__👌Bot para subir a las nubes  y descargar contenido sin consumir sus datos móviles__"
    return msg


def options():
    msg = "__📪Opciones__\n\n"
    msg += "__🌃Thumb: 👌Elige la imagén de los archivos__\n\n"
    msg += "__📝Caption: 👌Escribe un comentario para tus archivos__\n\n"
    msg += "__🔁Default: 👌Vuelve a la imagén y el comentario por defecto__\n\n"
    msg += "__📚Ext: 👌Elige la extensión de los archivos (zip,7z)__"
    return msg


def status(disk, ram, users_count, users, totalUpload):
    msg = "**——•Estado•——**\n\n"
    msg += f"**•Usuarios #: {str(users_count)}\n**"
    for user in users:
        msg += f"**-->{user} - {str(sizeof_fmt(totalUpload))}\n**"
    msg += f"**•Almacenamiento: {str(sizeof_fmt(disk.total))}\n**"
    msg += f"**•Disponible: {str(sizeof_fmt(disk.free))}\n**"
    msg += f"**•Ram: {str(sizeof_fmt(ram.total))}\n**"
    msg += f"**•Disponible: {str(sizeof_fmt(ram.available))}\n**"
    return msg
