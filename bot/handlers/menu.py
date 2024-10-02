from bot.handlers.sub import *
from math import ceil
import os

STATIC_FOLDER = f'{bot_basedir}/static'
EVENTS_PER_PAGE = 1

mocked_events = [
    {
        'id': 1,
        'title': 'Event 1',
        'description': 'Описание Event 1',
        'media': ['image1.jpg', 'image2.jpg'],
        'registration_link': 'https://example.com/register1',
        'telegram_link': 'https://t.me/example_event1',
        'instagram_link': 'https://instagram.com/example_event1'
    },
    {
        'id': 2,
        'title': 'Event 2',
        'description': 'Описание Event 2',
        'media': ['image1.jpg'],
        'registration_link': 'https://example.com/register2',
        'telegram_link': 'https://t.me/example_event2',
        'instagram_link': 'https://instagram.com/example_event2'
    },
]

async def show_main_menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Ивенты", callback_data="show_events"))
    keyboard.add(types.InlineKeyboardButton(text="Instagram", url="https://instagram.com/na.gasone"))
    keyboard.add(types.InlineKeyboardButton(text="Telegram", url="https://t.me/nagasone"))
    keyboard.add(types.InlineKeyboardButton(text="FAQ", callback_data="show_faq"))

    try:
        await bot.edit_message_text(
            "Выберите опцию:",
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=keyboard
        )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Выберите опцию:",
            reply_markup=keyboard
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('events_menu'))
async def events_menu_inline(call):
    try:
        page = int(call.data.split('#')[1])
    except IndexError:
        page = 1
    await events_menu(call, page=page, edit_message=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith('nullified'))
async def nullified(call):
    await bot.answer_callback_query(call.id, "Это текущая страница!")

async def events_menu(target, page=1, edit_message=False):
    all_events = mocked_events
    total_pages = ceil(len(all_events) / EVENTS_PER_PAGE)

    events_chunks = [all_events[i:i + EVENTS_PER_PAGE] for i in range(0, len(all_events), EVENTS_PER_PAGE)]
    events_to_display = events_chunks[page - 1] if page <= len(events_chunks) else []

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for event in events_to_display:
        keyboard.add(
            types.InlineKeyboardButton(text=f"Зарегистрироваться на {event['title']}", url=event['registration_link']))
        keyboard.add(
            types.InlineKeyboardButton(text="Telegram пост", url=event['telegram_link']),
            types.InlineKeyboardButton(text="Instagram пост", url=event['instagram_link'])
        )

    if total_pages > 1:
        prev_page = types.InlineKeyboardButton(text="<", callback_data=f"events_menu#{page - 1 if page > 1 else 1}")
        next_page = types.InlineKeyboardButton(text=">", callback_data=f"events_menu#{page + 1 if page < total_pages else total_pages}")
        page_info = types.InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="nullified")
        keyboard.add(prev_page, page_info, next_page)

    media_group = []
    text = ""

    for event in events_to_display:
        for media_file in event['media']:
            file_path = os.path.join(STATIC_FOLDER, media_file)
            if os.path.exists(file_path):
                media_group.append(types.InputMediaPhoto(open(file_path, 'rb')))
        text += f"<b>{event['title']}</b>\n{event['description']}\n\n"


    back_button = types.InlineKeyboardButton(text="Назад в главное меню", callback_data="back_to_main")
    keyboard.add(back_button)

    if edit_message and media_group:
        await bot.edit_message_media(media_group[0], chat_id=target.message.chat.id, message_id=target.message.message_id, reply_markup=keyboard)
        await bot.edit_message_text(text.strip(), chat_id=target.message.chat.id, message_id=target.message.message_id, parse_mode="html", reply_markup=keyboard)
    else:
        if media_group:
            await bot.send_media_group(target.message.chat.id, media_group)
        await bot.send_message(target.message.chat.id, text.strip(), parse_mode="html", reply_markup=keyboard)
