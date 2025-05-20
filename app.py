from flask import Flask, request
import telegram
import mysql.connector
import config

app = Flask(__name__)
bot = telegram.Bot(token=config.BOT_TOKEN)

@app.route(f'/{config.BOT_TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    user_message = update.message.text.strip()

    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        query = "SELECT username, password, expiration FROM rm_users WHERE username = %s"
        cursor.execute(query, (user_message,))
        user = cursor.fetchone()

        if user:
            msg = (
                f"👤 اسم المستخدم: {user['username']}\n"
                f"🔑 كلمة المرور: {user['password']}\n"
                f"📅 تاريخ الانتهاء: {user['expiration']}"
            )
        else:
            msg = "لم يتم العثور على الحساب. تأكد من إدخال اسم المستخدم بشكل صحيح."
    except Exception as e:
        msg = f"حدث خطأ في الاتصال: {str(e)}"
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    bot.sendMessage(chat_id=chat_id, text=msg)
    return 'ok'

import os
port = int(os.environ.get("PORT", 1000))
app.run(host="0.0.0.0", port=port)
