import asyncio
import traceback
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from pathlib import Path
import threading

from ...config import config
from ...core.loader import makeReader
from ..dependencies import get_core

from threading import Lock

lock = Lock()

def run_telegram_polling():
    core = get_core()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot = Bot(token=config.telegram_bot_token)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_cmd(message: types.Message):
        with lock:
            core.history_store.clear(message.from_user.id)
        await message.answer(
            "Привет! 👋\n\nОтправь документ (PDF, DOCX, RTF, MD или TXT), "
            "а затем задай вопросы по нему. Я буду помнить историю диалога."
        )

    @dp.message(F.document)
    async def handle_file(message: types.Message):
        document = message.document
        user_id = message.from_user.id

        UPLOAD_DIR = Path(config.upload_dir) / str(user_id)
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        file_path = UPLOAD_DIR / document.file_name

        file = await bot.download(document)
        with open(file_path, 'wb') as f:
            f.write(file.read())

        try:
            reader = makeReader(str(file_path))
            content = reader.read(str(file_path))
        except Exception as e:
            traceback.print_exc()
            await message.answer(f"Произошла ошибка на стороне сервера, пожалуйста, попробуйте позднее")
            return

        with lock:
            core.save_file(user_id=user_id, file_name=document.file_name, content=content)

        await message.answer("Файл получен и обработан ✅ Теперь задай вопрос.")

    @dp.message(F.text)
    async def handle_question(message: types.Message):
        user_id = message.from_user.id

        with lock:
            doc_content = core.user_store.get_content(user_id)

        if not doc_content:
            await message.answer("Сначала отправь мне документ 📄")
            return

        question = message.text
        await message.answer("Обрабатываю твой вопрос... ⏳")

        try:
            answer = await core.ask(user_id=user_id, question=question)
            await message.answer(f"💬 Ответ:\n\n{answer}")
        except Exception as e:
            traceback.print_exc()
            await message.answer(f"Произошла ошибка на стороне сервера, пожалуйста, попробуйте позднее")

    print("Starting Telegram polling...")
    loop.run_until_complete(dp.start_polling(bot))


def start_telegram_bot():
    t = threading.Thread(target=run_telegram_polling, daemon=True)
    t.start()
