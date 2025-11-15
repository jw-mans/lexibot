from aiogram import (
    Bot, Dispatcher, 
    types, F,
)
from aiogram.filters import Command

import asyncio
import os
from pathlib import Path

from ..config import config
from ..core.loader import makeReader
from ..core.core import Core

bot = Bot(token=config.telegram_bot_token)
dp = Dispatcher()

core = Core()

# TODO: Build Store

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    core.history_store.clear(message.from_user.id)
    await message.answer(
        "Привет! 👋\n\nОтправь мне документ (PDF, DOCX, RTF, MD или TXT), а потом задай вопрос по нему.\n"
        "Я запомню документ и буду отвечать на цепочку вопросов без повторной загрузки."
    )

@dp.message(F.document)
async def handle_file(message: types.Message):
    document = message.document
    file_path = Path(config.upload_dir) / document.file_name
    os.makedirs(file_path.parent, exist_ok=True)

    file = await bot.download(document)
    with open(file_path, 'wb') as f:
        f.write(file.read())

    try: 
        reader = makeReader(str(file_path))
        content = reader.read(str(file_path))
    except Exception as e:
        await message.answer(f"Не удалось прочитать файл: {e}")
        return
    
    Core.save_file(
        user_id=message.from_user.id,
        file_name=document.file_name,
        content=content
    )
    core.history_store.clear(message.from_user.id)
    await message.answer("Файл получен и обработан ✅ Теперь задай вопрос по нему.")

@dp.message(F.text)
async def handle_question(message: types.Message):
    user_id = message.from_user.id
    context = core.user_store.get_content(user_id)
    
    if not context:
        await message.answer("Сначала отправь мне документ для анализа 📄")
        return
    
    question = message.text
    await message.answer("Обрабатываю твой вопрос... ⏳")

    try: 
        answer = await core.ask(
            user_id=user_id,
            question=question,
        )

        await message.answer(f"💬 Ответ:\n\n{answer}")
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке вопроса: {e}")

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
