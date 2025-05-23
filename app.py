import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("5568994702:AAHTqFwIKRk0ka__RgEvlvDfA_BwAL0yD0c")

application = Application.builder().token(TOKEN).build()

def check_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        conn.close()
        print("✅ تم الاتصال بقاعدة البيانات بنجاح")
    except Exception as e:
        print(f"❌ فشل الاتصال بقاعدة البيانات: {e}")

check_db_connection()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً، هذا بوت لعرض معلومات حساب Radius Manager.")

application.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return "ok", 200
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return "error", 500

@app.route("/", methods=["GET"])
def index():
    return "🚀 البوت يعمل بشكل سليم"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run_polling()
    app.run(host="0.0.0.0", port=port)
