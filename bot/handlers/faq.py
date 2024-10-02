from bot.config import *

@bot.callback_query_handler(func=lambda call: call.data == 'show_faq')
async def show_faq(call):
    faq_text = "Это раздел FAQ. Здесь вы можете узнать о нашем боте и его функциях."
    await bot.edit_message_text(
        faq_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="html"
    )