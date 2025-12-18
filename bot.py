import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import aiohttp

TELEGRAM_TOKEN = "8504317181:AAHk-3QnxkCV57hIzaQh6UpqTGHplozd7go"

PERPLEXITY_API_KEY = "pplx-YOUR_API_KEY_HERE"

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
            
            prompt = f"""Ты профессиональный стилист. Пользователь написал: "{user_message}"

Подбери 3-5 рекомендаций образа, учитывая город, повод ,стиль,возраст
Включи названия брендов и ссылки на Wildberries/Ozon.
Ответь КРАТКО на русском (4-6 предложений)."""

            data = {
                "model": "sonar",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500
            }
            
            async with session.post(
                "https://api.perplexity.ai/chat/completions",
                json=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    return f"Ошибка API: {response.status}"
                    
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("""🌍 Привет! Я Style Geo — твой персональный ИИ‑стилист.  
Подскажу, что надеть под твоё настроение или конкретный повод — и сразу дам ссылки на вещи, которые можно приобрести онлайн.
Напиши, пожалуйста:
1️⃣ Город и страну  
2️⃣ Для какой ситуации подбираем образ (работа, учёба, свидание, прогулка,мероприятие)  
3️⃣ Твой повседневный стиль одежды (casual, спорт, классика и т.п.)  
4️⃣ Возраст (можно диапазон: до 25, 25–35, 35–45, 45+)  
5️⃣ Телосложение (стройное, среднее,или опиши своими словами)
 Расскажи о себе честно — и тогда я ворвусь в роль стилиста и соберу тебе образ, в котором захочется делать селфи и спамить фото в соцсетях, а не прятаться 😉

@dp.message()
async def handle_message(message: types.Message):
    """Ловит все сообщения и отправляет в Perplexity"""
    try:
        await bot.send_chat_action(message.chat.id, "typing")
        response = await ask_perplexity(message.text)
        await message.answer(response)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)[:100]}")

async def main():
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
