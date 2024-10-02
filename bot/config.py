import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup

load_dotenv()

CHANNEL_ID = os.getenv("GASON_GROUP_CHATID")

bot = AsyncTeleBot(
    os.getenv("TELEGRAM_BOT_TOKEN"),
    state_storage=StateMemoryStorage(),
    disable_notification=False,
    colorful_logs=True
)

EVENT_PER_PAGE = 1
msg_ids = dict()

class UserStates(StatesGroup):
    start = State()
    share_contact = State()
    subscribe = State()
    main_menu = State()
    faq = State()

class AdminStates(StatesGroup):
    pass

bot_basedir = os.path.abspath(os.path.dirname(__file__))