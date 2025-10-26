from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram import F
import asyncio
import os
from pathlib import Path

from ..config import settings
from ..core.loader import makeReader
from ..core.llm.client import GPTClient
from ..core.llm.pipeline import Pipeline

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

client = GPTClient()
pipeline = Pipeline(client)


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Привет! Отправь мне документ (PDF, DOCX, RTF, MD или TXT), а потом задай вопрос по нему.")


USER_CONTEXTS = {}


@dp.message(F.document)
async def handle_file(message: types.Message):
    document = message.document
    file_path = Path(settings.UPLOAD_DIR) / document.file_name
    os.makedirs(file_path.parent, exist_ok=True)

    file = await bot.download(document)
    with open(file_path, "wb") as f:
        f.write(file.read())

    try:
        reader = makeReader(str(file_path))
        content = reader.read(str(file_path))
    except Exception as e:
        await message.answer(f"Ошибка чтения файла: {e}")
        return

    USER_CONTEXTS[message.from_user.id] = content
    await message.answer("Файл получен и обработан ✅ Теперь задай вопрос по нему.")


@dp.message(F.text)
async def handle_question(message: types.Message):
    user_id = message.from_user.id
    if user_id not in USER_CONTEXTS:
        await message.answer("Сначала отправь документ 📄")
        return

    context = USER_CONTEXTS[user_id]
    question = message.text
    await message.answer("⏳ Думаю...")

    try:
        answer = pipeline.ask(context, question)
        await message.answer(f"💬 Ответ:\n\n{answer}")
    except Exception as e:
        await message.answer(f"Ошибка при обращении к YandexGPT: {e}")


async def main():
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
