import os
import logging
import zipfile
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import Router
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv
import asyncio
from pathlib import Path
import time
import shutil

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

try:
    bot = Bot(token=TOKEN)
except TokenValidationError as e:
    logging.error(f"🔴 Invalid token: {e}")
    exit()

dp = Dispatcher(storage=MemoryStorage())

router = Router()

CALIBRE_CONVERT_COMMAND = 'ebook-convert'

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

FILE_LIFETIME = 1200


def check_calibre_available():
    calibre_path = shutil.which(CALIBRE_CONVERT_COMMAND)
    if not calibre_path:
        logging.error(f"🔴 Calibre not found! Please ensure it is installed and accessible in the system.")
        return False

    return True


async def run_command(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    return stdout.decode(), stderr.decode(), process.returncode


@router.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer("Hello! 👋😃 Send me a .fb2 file, and I will convert it to .epub! 📚")


async def convert_fb2_to_epub(fb2_file_path: Path, epub_file_path: Path):
    cmd = f"{CALIBRE_CONVERT_COMMAND} {fb2_file_path} {epub_file_path}"
    stdout, stderr, returncode = await run_command(cmd)

    if returncode != 0:
        logging.error(f"🔴 Conversation error: {stderr}")
        raise Exception(f"🔴 Conversation error: {stderr}")

    logging.info(f"🟢 Conversion completed: {stdout}")
    return epub_file_path


async def extract_epub_thumbnail(epub_file_path: Path, thumbnail_path: Path):
    try:
        with zipfile.ZipFile(epub_file_path, 'r') as epub:
            for file_info in epub.infolist():
                if 'cover' in file_info.filename and file_info.filename.endswith(('.jpg', '.jpeg', '.png')):
                    with open(thumbnail_path, 'wb') as thumbnail_file:
                        thumbnail_file.write(epub.read(file_info.filename))
                    logging.info(f"🟢 Cover image extracted: {thumbnail_path}")
                    return thumbnail_path
        return None
    except Exception as e:
        logging.error(f"🔴 Error extracting cover image: {e}")
        return None


@router.message(F.document)
async def handle_document(message: Message):
    document = message.document

    if not document.file_name.endswith('.fb2'):
        await message.answer(
            "Oh, it looks like you sent something incorrect! 😅📄\n"
            "Please send me a .fb2 file, and I’ll turn it into a stunning .epub! 📚✨", disable_notification=True)
        return

    file_info = await bot.get_file(document.file_id)

    file_name = document.file_name
    fb2_file_path = DATA_DIR / file_name  # Сохраняем файл в папку data
    epub_file_path = fb2_file_path.with_suffix('.epub')

    try:
        await bot.download_file(file_info.file_path, fb2_file_path.as_posix())

        converting_message = await message.answer("⏳ Converting...", disable_notification=True)

        await convert_fb2_to_epub(fb2_file_path, epub_file_path)

        thumbnail_path = DATA_DIR / (fb2_file_path.stem + '_thumbnail.jpg')
        thumbnail = await extract_epub_thumbnail(epub_file_path, thumbnail_path)

        thumb = None
        if thumbnail and thumbnail.exists():
            thumb = FSInputFile(thumbnail)

        await bot.send_document(
            chat_id=message.chat.id,
            reply_to_message_id=message.message_id,
            parse_mode='HTML',
            document=FSInputFile(
                path=epub_file_path.as_posix(),
                filename=epub_file_path.name),
            thumbnail=thumb)

        await converting_message.delete()

    except Exception as e:
        await message.answer(f"🔴 Oh no! Something went wrong! 😓 Error: {e}")
        logging.error(f"🔴 Error: {e}")


@router.message()
async def handle_all_messages(message: Message):
    await message.answer(
        "📗 Hey, I’m waiting for the .fb2 file! 😎\n"
        "Send it to me, and I’ll turn it into an .epub like magic! ✨\n"
        "Other files aren’t as interesting to me, but I believe you have just what I need. 😉")


async def cleanup_old_files():
    while True:
        now = time.time()
        for file_path in DATA_DIR.iterdir():
            if file_path.is_file() and (now - file_path.stat().st_mtime > FILE_LIFETIME):
                try:
                    file_path.unlink()
                    logging.info(f"🟢 Deleted: {file_path}")
                except Exception as e:
                    logging.error(f"🔴 Error deleting file {file_path}: {e}")
        await asyncio.sleep(60)


async def run_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await asyncio.gather(
        dp.start_polling(bot),
        cleanup_old_files())


def main():
    dp.include_router(router)

    if not check_calibre_available():
        logging.error("🔴 The bot has been stopped because Calibre is unavailable.")
        return

    logging.info('🚀 Bot is starting... ')
    asyncio.run(run_bot())


if __name__ == '__main__':
    main()
