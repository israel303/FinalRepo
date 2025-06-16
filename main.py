import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from utils import add_thumbnail
from tempfile import NamedTemporaryFile

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_docs(message: types.Message):
    file = message.document
    if not file.file_name.endswith((".pdf", ".epub")):
        await message.reply("📎 אני מקבל רק קבצי PDF או EPUB, חבוב 😎")
        return

    await message.reply("⏳ מעבד את הקובץ שלך...")
    file_path = await file.download()

    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.file_name)[-1]) as temp_output:
        output_path = temp_output.name

    try:
        add_thumbnail(file_path.name, output_path)
        new_name = "Oldtown_" + file.file_name
        await message.reply_document(types.InputFile(output_path, filename=new_name), caption="הקובץ מוכן! 📦")
    except Exception as e:
        await message.reply("❌ אופס! קרתה תקלה. נסה שוב מאוחר יותר.")
        logging.exception(e)
    finally:
        os.remove(file_path.name)
        if os.path.exists(output_path):
            os.remove(output_path)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("שלח לי קובץ PDF או EPUB ואחזיר לך אותו עם עטיפה קבועה ותגית 'Oldtown' בשם 😉")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
