from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import logging
import ErrorHandler
import requests
import json
import asyncio


async def check_user(user_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE):
    result: bool = await json.loads(requests.request("GET", f"https://api.cas.chat/check?user_id={user_id}").text)["ok"]
    if result:
        message = f"User {user_id} has been banned for CAS Violation."
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def on_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.new_chat_members[0].id
    await check_user(user_id, update, context)


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.new_chat_members[0].id
    await check_user(user_id, update, context)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    token = open("token.txt", "r+").readline().strip()
    app = ApplicationBuilder().token(token).build()
    app.add_error_handler(ErrorHandler.error_handler)
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_join))
    app.add_handler(MessageHandler(filters.TEXT, on_message))

    app.run_polling()
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
