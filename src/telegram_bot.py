from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)


from llm import GeminiBot

import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
user_dict={}

gemini_bot = GeminiBot(sheets_path = "delivery/planilhasap.xlsx")

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    print(user_id)


async def on_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    if user_id in user_dict.keys():
        print("on_message")
        message_id = update.message.message_id
        reaction = "👍"
        await context.bot.setMessageReaction(chat_id=chat_id, message_id=message_id, reaction=reaction)
        historico = user_dict[user_id]

        message_text = update.message.text

        bot_answer = gemini_bot.invoke(message_text)

        await context.bot.send_message(chat_id=chat_id,text=bot_answer)

    else:
        message = update.message
        message_text = message.text
        chat_id = update.effective_chat.id
        user_dict[user_id] = message_text

        bot_answer = gemini_bot.invoke(message_text)

        await context.bot.send_message(chat_id=chat_id,
                                    text=bot_answer,
                                    )
        
        user_dict[user_id] = f"user: {message_text}\n\nassistant:{bot_answer}"

application = Application.builder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.ALL, on_message))
print("ok")
application.run_polling()