import os
import json
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telegram import Bot

# Загружаем данные из .env
load_dotenv()
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUPS_TO_PARSE = list(map(int, os.getenv("TELEGRAM_GROUPS").split(',')))
SUBSCRIBERS_FILE = "subscribers.json"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Telethon клиент (второй аккаунт)
client = TelegramClient("session", API_ID, API_HASH)

# Создаем бота для отправки сообщений
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def load_subscribers():
    """Загружаем подписчиков"""
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    with open(SUBSCRIBERS_FILE, "r") as f:
        return json.load(f)

async def send_message_to_subscribers(message_text):
    """Отправляет сообщение подписчикам"""
    subscribers = load_subscribers()
    if subscribers:
        for user_id in subscribers:
            try:
                await bot.send_message(chat_id=user_id, text=f"📢 Новое сообщение:\n\n{message_text}")
            except Exception as e:
                logger.error(f"Ошибка при отправке пользователю {user_id}: {e}")

async def parse_telegram_groups():
    """Запускает мониторинг групп"""
    await client.start()

    @client.on(events.NewMessage(chats=GROUPS_TO_PARSE))
    async def handler(event):
        message_text = event.message.message
        logger.info(f"🔄 Новое сообщение из группы: {message_text}")
        await send_message_to_subscribers(message_text)

    print("🛠 Парсер работает...")
    await client.run_until_disconnected()


async def send_message_to_subscribers(message_text):
    """Отправляет сообщение подписчикам"""
    subscribers = load_subscribers()
    print(f"👥 Подписчики: {subscribers}")  # Проверяем подписчиков
    if subscribers:
        for user_id in subscribers:
            try:
                print(f"📨 Отправка сообщения пользователю {user_id}...")
                await bot.send_message(chat_id=user_id, text=f"📢 Новое сообщение:\n\n{message_text}")
                print(f"✅ Отправлено пользователю {user_id}")
            except Exception as e:
                logger.error(f"Ошибка при отправке пользователю {user_id}: {e}")
                print(f"❌ Ошибка при отправке пользователю {user_id}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(parse_telegram_groups())
