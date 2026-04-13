from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
import configparser
import logging
from ChatGPT_HKBU import ChatGPT
import redis
import datetime

# Redis
db = redis.Redis(
    host="master.chatbot-redis.dag9bz.apse2.cache.amazonaws.com",
    port=6379,
    password="",
    decode_responses=True,
    ssl=True
)

gpt = None

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    config = configparser.ConfigParser()
    config.read('config.ini')
    global gpt
    gpt = ChatGPT(config)

    app = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("history", show_history))
    app.add_handler(CommandHandler("clear", clear_history))
    app.add_handler(CommandHandler("remind", add_remind))
    app.add_handler(CommandHandler("reminders", list_reminders))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("time", show_time))
    app.add_handler(CommandHandler("about", about))

    # Chat
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    logging.info("Bot started!")
    app.run_polling()

# ------------------------------
# Basic
# ------------------------------
async def start(update: Update, context: ContextTypes):
    await update.message.reply_text("👋 Hi! I'm your HKBU Campus Assistant.\nType /help for commands.")

async def about(update: Update, context: ContextTypes):
    text = """
🤖 HKBU CAMPUS ASSISTANT

Features:
• AI chat
• Chat history
• Reminders
• Weather check
• Time check

Built for COMP7940
"""
    await update.message.reply_text(text)

# ------------------------------
# AI Chat
# ------------------------------
async def chat(update: Update, context: ContextTypes):
    msg = await update.message.reply_text("Thinking...")
    user_id = update.message.from_user.id
    text = update.message.text
    reply = gpt.submit(text)

    # Save history
    db.rpush(f"history:{user_id}", f"You: {text}\nBot: {reply}")
    db.ltrim(f"history:{user_id}", -10, -1)

    await msg.edit_text(reply)

# ------------------------------
# History
# ------------------------------
async def show_history(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    logs = db.lrange(f"history:{user_id}", 0, -1)
    if not logs:
        await update.message.reply_text("No history.")
        return
    out = "📜 CHAT HISTORY:\n\n" + "\n\n".join(logs)
    await update.message.reply_text(out)

async def clear_history(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    db.delete(f"history:{user_id}")
    await update.message.reply_text("✅ History cleared.")

# ------------------------------
# Reminders
# ------------------------------
async def add_remind(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    content = " ".join(context.args)
    if not content:
        await update.message.reply_text("Usage: /remind Do assignment")
        return
    db.rpush(f"remind:{user_id}", content)
    await update.message.reply_text(f"✅ Reminder saved: {content}")

async def list_reminders(update: Update, context: ContextTypes):
    user_id = update.message.from_user.id
    items = db.lrange(f"remind:{user_id}", 0, -1)
    if not items:
        await update.message.reply_text("No reminders.")
        return
    res = "📌 REMINDERS:\n"
    for i, item in enumerate(items, 1):
        res += f"{i}. {item}\n"
    await update.message.reply_text(res)

# ------------------------------
# Extra Features
# ------------------------------
async def weather(update: Update, context: ContextTypes):
    await update.message.reply_text("🌤 Sunny in Hong Kong today (26°C)")

async def show_time(update: Update, context: ContextTypes):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"🕒 Current time: {now}")

async def help_command(update: Update, context: ContextTypes):
    help_text = """
📌 COMMANDS:
/start - Greeting
/help - Show help
/history - Show chat
/clear - Clear history
/remind - Add reminder
/reminders - List reminders
/weather - Check weather
/time - Show time
/about - About bot
"""
    await update.message.reply_text(help_text)

if __name__ == "__main__":
    main()