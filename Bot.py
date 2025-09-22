import telebot
import logging

# ✅ Replace with your bot token in quotes
BOT_TOKEN = "8131672831:AAFTee1s4JBO_zdyi4V-BYjksI3hJ3HvAyk"
bot = telebot.TeleBot(BOT_TOKEN)

# ✅ Replace with your real IDs
GROUP_CHAT_ID = -1003032968701   # group chat ID (must start with -100)
DOCTOR_USER_ID = 7955253738       # doctor’s private user ID

# Setup logging
logging.basicConfig(
    filename="bridge_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Forward from group -> doctor
@bot.message_handler(func=lambda m: m.chat.id == GROUP_CHAT_ID)
def group_to_doctor(message):
    try:
        if message.content_type == 'text':
            bot.send_message(DOCTOR_USER_ID, f"👥 Patient: {message.text}")
        else:
            bot.forward_message(DOCTOR_USER_ID, GROUP_CHAT_ID, message.message_id)
        # ✅ Confirmation in group
        bot.send_message(GROUP_CHAT_ID, "✅ Sent to doctor")
    except Exception as e:
        logging.error(f"Group → Doctor failed: {e}")
        bot.send_message(DOCTOR_USER_ID, f"⚠️ Error (Group→Doctor): {e}")

# Forward from doctor -> group
@bot.message_handler(func=lambda m: m.chat.id == DOCTOR_USER_ID)
def doctor_to_group(message):
    try:
        if message.content_type == 'text':
            bot.send_message(GROUP_CHAT_ID, f"👨‍⚕️ Doctor: {message.text}")
        else:
            bot.forward_message(GROUP_CHAT_ID, DOCTOR_USER_ID, message.message_id)
        # ✅ Confirmation to doctor
        bot.send_message(DOCTOR_USER_ID, "✅ Sent to group")
    except Exception as e:
        logging.error(f"Doctor → Group failed: {e}")
        bot.send_message(DOCTOR_USER_ID, f"⚠️ Error (Doctor→Group): {e}")

print("🚀 Telegram bridge is running...")
bot.infinity_polling()
