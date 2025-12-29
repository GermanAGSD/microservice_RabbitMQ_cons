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
from pydantic import BaseModel
from utils import get_ip
# Bot token can be obtained via https://t.me/BotFather


broker = RabbitBroker("amqp://admin:admin123@172.30.30.19:5672/")
TOKEN = "7975223905:AAGRlxuXhOU1OjvMyNnYdpRqJq08qC5OLig"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
CHAT_ID = 2037339309

class JsonMessage(BaseModel):
    id: int
    event: str
    message: str




@broker.subscriber("orders")
async def handle_orders_and_message(msg: JsonMessage):
    payload = msg.model_dump_json()

    match msg.event:
        case "send_ip":
            ip =get_ip()
            logging.info(f"ip address отправлен на сервер {ip}")
            msg.message = ip  # кладём IP в поле message
            await bot.send_message(CHAT_ID, text=msg.model_dump_json(indent=3))
        case _:
            logging.error("Неизвестный тип данных")

    # print(payload)
    # await bot.send_message(CHAT_ID, text=msg.model_dump_json(indent=2))

@broker.subscriber("product")
async def on_product(data: str):
    await bot.send_message(CHAT_ID, text=data)

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
