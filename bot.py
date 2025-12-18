import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import aiohttp
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

async def ask_perplexity(user_message):
    """Отправляет запрос в Perplexity API"""
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "pplx-7b-online",
                "messages": [{"role": "user", "content": user_message}]
            }
            async with session.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers) as resp:
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка: {str(e)}"

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Я AI-стилист. Расскажи о своём стиле, и я подберу рекомендации!")

@dp.message()
async def handle_message(message: types.Message):
    response = await ask_perplexity(message.text)
    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
