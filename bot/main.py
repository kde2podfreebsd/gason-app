import asyncio
import logging
from telebot.asyncio_filters import (
    ForwardFilter,
    IsDigitFilter,
    IsReplyFilter,
    StateFilter,
)
from flood import FloodingMiddleware
from bot.handlers import *

logging.basicConfig(level=logging.INFO)


class Bot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        bot.add_custom_filter(IsReplyFilter())
        bot.add_custom_filter(ForwardFilter())
        bot.add_custom_filter(StateFilter(bot))
        bot.add_custom_filter(IsDigitFilter())

        bot.setup_middleware(FloodingMiddleware(1))

    @staticmethod
    def polling():
        asyncio.run(bot.infinity_polling())


if __name__ == "__main__":
    Bot().polling()