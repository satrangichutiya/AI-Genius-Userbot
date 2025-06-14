from AdityaHalder.modules.clients.clients import call
from .streams import run_stream, get_result, get_stream

async def run_async_calls(chat_id, query, stream_type="Audio"):
    # Get YouTube URL and thumbnail
    url, thumbnail = await get_result(query)

    # Download audio/video file
    file = await get_stream(url, stream_type)

    # Prepare AudioPiped stream (video removed for compatibility)
    stream = await run_stream(file, "Audio")

    # Join group call with the audio stream
    await call.join_group_call(chat_id, stream)
