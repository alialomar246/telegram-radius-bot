from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = "8010087659:AAHKI0K8nC243YwIrITUv8e_QsC2_81rOfI"
bot = Bot(token=TOKEN)
app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا، هذا بوت تيليجرام متصل بقاعدة Radius Manager.")

application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    async def handle_update():
        await application.process_update(update)

    asyncio.run(handle_update())
    return "ok"

# صفحة فحص
@app.route("/", methods=["GET"])
def index():
    return "البوت يعمل ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
