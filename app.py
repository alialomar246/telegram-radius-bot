from flask import Flask, request
import mysql.connector
import telegram
from telegram import Update
import asyncio
import config

app = Flask(__name__)
bot = telegram.Bot(token=config.BOT_TOKEN)

async def handle_message(update: Update):
    msg = update.message.text.strip()
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, credit, expiration FROM rm_users WHERE username = %s", (msg,))
        row = cursor.fetchone()
        if row:
            reply = f"""📄 *بيانات الحساب:*\n👤 المستخدم: `{row['username']}`\n💳 الرصيد: `{row['credit']}`\n📅 الانتهاء: `{row['expiration']}`"""
        else:
            reply = "❌ الحساب غير موجود، تحقق من الرقم."
        await bot.send_message(chat_id=update.message.chat.id, text=reply, parse_mode='Markdown')
    except Exception as e:
        await bot.send_message(chat_id=update.message.chat.id, text="حدث خطأ أثناء الاستعلام.")
        print(e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route(f"/{config.BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    asyncio.run(handle_message(update))
    return "ok"

@app.route("/", methods=["GET"])
import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
def home():
    return "بوت Telegram Radius يعمل ✅"
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
