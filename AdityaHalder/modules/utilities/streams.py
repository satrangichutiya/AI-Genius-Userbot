import os
import asyncio
import yt_dlp

from . import queues
from ..clients.clients import call
from ...console import USERBOT_PICTURE

from asyncio.queues import QueueEmpty
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from youtubesearchpython.__future__ import VideosSearch


async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


async def get_result(query: str):
    results = VideosSearch(query, limit=1)
    try:
        result = (await results.next())["result"][0]
        url = result["link"]
        thumbnail = result.get("thumbnails", [{}])[0].get("url", "").split("?")[0] or USERBOT_PICTURE
        return url, thumbnail
    except Exception:
        return None, USERBOT_PICTURE


async def get_stream(link, stream_type="Audio"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }

    ydl = yt_dlp.YoutubeDL(ydl_opts)
    info = ydl.extract_info(link, download=False)
    file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")

    if os.path.exists(file_path):
        return file_path

    await run_async(ydl.download, [link])
    return file_path


async def run_stream(file, stream_type="Audio"):
    return AudioPiped(
        file,
        HighQualityAudio()
    )


async def close_stream(chat_id):
    try:
        await queues.clear(chat_id)
    except QueueEmpty:
        pass
    try:
        await call.leave_group_call(chat_id)
    except:
        pass
