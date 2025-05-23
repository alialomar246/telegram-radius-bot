import os
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from flask import Flask, request
import mysql.connector

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")  # ← تأكد أنه مسجل في بيئة التشغيل
application = Application.builder().token(TOKEN).build()

# تحقق من الاتصال بقاعدة البيانات
def check_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        conn.close()
        print("✅ تم الاتصال بقاعدة البيانات بنجاح!")
    except Exception as e:
        print(f"❌ فشل الاتصال بقاعدة البيانات: {e}")

check_db_connection()

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 البوت يعمل بنجاح!")

application.add_handler(CommandHandler("start", start))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.run_async(application.process_update(update))
        return "ok", 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return "error", 500

@app.route("/", methods=['GET'])
def index():
    return "✅ البوت يعمل"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
