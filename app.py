from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import mysql.connector
import asyncio
import os

TOKEN = "8010087659:AAHKI0K8nC243YwIrITUv8e_QsC2_81rOfI"
bot = Bot(token=TOKEN)

DB_HOST = "46.235.15.27"
DB_NAME = "radius"
DB_USER = "radius"
DB_PASS = "radius123"

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

def get_user_info(username):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, credit, expiration FROM rm_users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"DB error: {e}")
        return None

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_username = update.message.from_user.username
    if not tg_username:
        await update.message.reply_text("@Alialomar_bot")
        return

    user = get_user_info(tg_username)
    if user:
        msg = f"""📄 معلومات حسابك:
👤 المستخدم: {user['username']}
💰 الرصيد: {user['credit']}
📅 تاريخ الانتهاء: {user['expiration']}
"""
    else:
        msg = "❌ لم يتم العثور على بيانات حسابك. تأكد من تطابق اسم المستخدم مع بيانات الشبكة."
    await update.message.reply_text(msg)

# إضافة المعالج
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

# ربط Webhook مع Flask
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "🤖 Bot is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
