from pyrogram.types import Message
from ...clients.clients import call
from .streams import run_stream, get_result, get_stream

async def run_async_calls(chat_id, query, stream_type="Audio"):
    url, thumbnail = await get_result(query)
    file = await get_stream(url, stream_type)

    if stream_type == "Audio":
        stream = await run_stream(file, "Audio")
        await call.join_group_call(chat_id, stream)
    elif stream_type == "Video":
        audio, video = await run_stream(file, "Video")
        await call.join_group_call(chat_id, audio, video)
