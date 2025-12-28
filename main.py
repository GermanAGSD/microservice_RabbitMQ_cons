import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from faststream.rabbit import RabbitBroker
from aiogram.types import Message
# Bot token can be obtained via https://t.me/BotFather


broker = RabbitBroker("amqp://admin:admin123@172.30.30.19:5672/")
TOKEN = "7975223905:AAGRlxuXhOU1OjvMyNnYdpRqJq08qC5OLig"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@broker.subscriber("orders")
async def handle_orders_and_message(data: str):
    await bot.send_message(
        chat_id=2037339309,
        text=data
    )
# Узнать id chat room
# @dp.message()
# async def handle_message(msg: Message):
#     await msg.answer(f"Ваш id {msg.chat.id}")

async def main() -> None:
    async with broker:
        await broker.start()
        logging.info("Брокер старт")
        await dp.start_polling(bot)
    logging.info("Stop broker")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())