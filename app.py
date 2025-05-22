from flask import Flask, request
import mysql.connector
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters
import logging
import os

TOKEN = "8010087659:AAHKI0K8nC243YwIrITUv8e_QsC2_81rOfI"
bot = Bot(token=TOKEN)

DB_HOST = "46.235.15.27"
DB_NAME = "radius"
DB_USER = "radius"
DB_PASS = "radius123"

app = Flask(__name__)

dispatcher = Dispatcher(bot=bot, update_queue=None)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_user_info(username):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT username, credit, expiration FROM rm_users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

def reply(update: Update, context):
    tg_username = update.message.from_user.username
    if not tg_username:
        update.message.reply_text("@Alialomar_bot")
        return

    user = get_user_info(tg_username)
    if user:
        msg = f"""📄 معلومات حسابك:
👤 المستخدم: {user['username']}
💰 الرصيد: {user['credit']}
📅 تاريخ الانتهاء: {user['expiration']}
"""
    else:
        msg = "❌ لم يتم العثور على بيانات حسابك. تأكد من أن اسم المستخدم في تيليجرام يطابق اسم المستخدم في الشبكة."
    update.message.reply_text(msg)

dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "🤖 Bot is live"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
