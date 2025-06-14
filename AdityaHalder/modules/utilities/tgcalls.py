from AdityaHalder.modules.clients.clients import call
from .streams import run_stream, get_result, get_stream


async def run_async_calls(chat_id, query, stream_type="Audio"):
    try:
        # Search YouTube and get the video URL
        url, thumbnail = await get_result(query)

        if not url:
            print("❌ No result found for query.")
            return

        # Download streamable file (audio)
        file = await get_stream(url, stream_type)

        # Prepare stream object (AudioPiped)
        stream = await run_stream(file, stream_type)

        # Join group call
        await call.join_group_call(chat_id, stream)
        print(f"✅ Joined VC in {chat_id} with query: {query}")

    except Exception as e:
        print(f"⚠️ Error in run_async_calls: {e}")
