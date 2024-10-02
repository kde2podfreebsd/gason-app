from bot.config import *
from telebot import types

@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
async def check_sub(call):
    user_id = call.message.chat.id
    if await is_user_subscribed(user_id):
        await bot.delete_message(user_id, call.message.message_id)
        await show_main_menu(call.message)
    else:
        markup = get_subscription_markup()
        await bot.edit_message_text(
            "Вы не подписались:(\nПожалуйста, подпишитесь на наш канал, чтобы использовать бота. [Подписаться](https://t.me/nagasone)",
            chat_id=user_id,
            message_id=call.message.message_id,
            parse_mode='Markdown'
        )
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

async def is_user_subscribed(user_id):
    try:
        sub_status = await bot.get_chat_member(CHANNEL_ID, user_id)
        return sub_status.status != 'left'
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False

def get_subscription_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='Подписаться!', url="https://t.me/nagasone"))
    markup.add(types.InlineKeyboardButton(text='Проверить подписку', callback_data="check_sub"))
    return markup

async def send_subscription_message(chat_id):
    markup = get_subscription_markup()
    msg = await bot.send_message(
        chat_id,
        "Пожалуйста, подпишитесь на наш канал, чтобы использовать бота. [Подписаться](https://t.me/nagasone)",
        parse_mode='Markdown',
        reply_markup=markup
    )
    msg_ids[chat_id] = msg.id

async def back_to_main_menu(call):
    await show_main_menu(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
async def back(call):
    await back_to_main_menu(call)

