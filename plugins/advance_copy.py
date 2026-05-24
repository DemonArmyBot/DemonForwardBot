# plugins/advanced_copy.py
import os
import asyncio
from pyrogram.errors import FloodWait

async def advanced_copy(user, bot, msg, m, sts):
    """
    Strong bypass for CHAT_FORWARDS_RESTRICTED
    Downloads the file and re-uploads it as new media.
    """
    try:
        file_id = msg.get("media")
        caption = msg.get("caption")
        button = msg.get('button')
        protect = msg.get("protect")
        media_type = msg.get("media_type")
        is_video = msg.get("video", False)

        if not file_id:
            # Fallback to normal copy for text messages
            return await bot.copy_message(
                chat_id=sts.get('TO'),
                from_chat_id=sts.get('FROM'),
                message_id=msg.get("msg_id"),
                reply_markup=button,
                protect_content=protect
            )

        # Download
        downloaded = await bot.download_media(file_id)

        if is_video or media_type == "video":
            await bot.send_video(
                chat_id=sts.get('TO'),
                video=downloaded,
                caption=caption,
                reply_markup=button,
                protect_content=protect,
                supports_streaming=True
            )
        else:
            # Default to document (safest for most files)
            await bot.send_document(
                chat_id=sts.get('TO'),
                document=downloaded,
                caption=caption,
                reply_markup=button,
                protect_content=protect
            )

        # Cleanup
        if downloaded and os.path.exists(downloaded):
            os.remove(downloaded)

        return True

    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await advanced_copy(user, bot, msg, m, sts)

    except Exception as e:
        print(f"Advanced Copy Error: {e}")
        raise e