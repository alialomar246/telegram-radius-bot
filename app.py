from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import mysql.connector
import os
from flask import Flask, request

app = Flask(__name__)

# توكن البوت من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")
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

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 البوت يعمل بنجاح!")

application.add_handler(CommandHandler("start", start))

# نقطة استقبال التحديثات من تيليجرام (Webhook)
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(), application.bot)
        application.run_async(application.process_update(update))
        return "ok", 200
    except Exception as e:
        print(f"Error in webhook: {e}")
        return "error", 500

# نقطة فحص الخدمة
@app.route('/', methods=['GET'])
def index():
    return "البوت يعمل ✅"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
