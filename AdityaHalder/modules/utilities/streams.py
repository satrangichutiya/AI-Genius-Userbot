import asyncio
import os
import yt_dlp

from . import queues
from ..clients.clients import call
from ...console import USERBOT_PICTURE

from asyncio.queues import QueueEmpty
from pytgcalls.types.stream import Stream
from pytgcalls.types.stream.audio_stream import AudioPiped
from pytgcalls.types.stream.video_stream import VideoPiped
from pytgcalls.types.stream import AudioParameters, VideoParameters
from youtubesearchpython.__future__ import VideosSearch


async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


async def get_result(query: str):
    results = VideosSearch(query, limit=1)
    result = (await results.next())["result"][0]
    url = result["link"]
    thumbnail = result.get("thumbnails", [{}])[0].get("url", USERBOT_PICTURE).split("?")[0]
    return url, thumbnail


async def get_stream(link, stream_type):
    ydl_opts = {
        "format": "bestaudio/best" if stream_type == "Audio" else "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }

    ydl = yt_dlp.YoutubeDL(ydl_opts)
    info = ydl.extract_info(link, download=False)
    file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")
    if not os.path.exists(file_path):
        await run_async(ydl.download, [link])
    return file_path


async def run_stream(file, stream_type):
    audio = AudioPiped(
        path=file,
        parameters=AudioParameters(
            bitrate=48000,
            channels=2,
        ),
    )

    if stream_type == "Audio":
        return Stream(audio)

    elif stream_type == "Video":
        video = VideoPiped(
            path=file,
            parameters=VideoParameters(
                width=1280,
                height=720,
                frame_rate=30,
            ),
        )
        return Stream(audio, video)


async def close_stream(chat_id):
    try:
        await queues.clear(chat_id)
    except QueueEmpty:
        pass
    try:
        return await call.leave_group_call(chat_id)
    except Exception:
        pass
