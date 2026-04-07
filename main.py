import os
import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator

TOKEN = os.getenv("BOT_TOKEN")
translator = Translator()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 AI Bot is Live!")

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        file = await update.message.document.get_file()
        os.makedirs("files", exist_ok=True)
        file_path = f"files/{update.message.document.file_name}"
        await file.download_to_drive(file_path)
        await update.message.reply_text("✅ File saved!")

def search_movie(name):
    for file in os.listdir("files"):
        if name.lower() in file.lower():
            return file
    return None

async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = " ".join(context.args)
    file = search_movie(name)

    if file:
        await update.message.reply_document(open(f"files/{file}", "rb"))
    else:
        await update.message.reply_text("❌ Not found")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    translated = translator.translate(text, src='hi', dest='ta')
    await update.message.reply_text("🌐 Tamil:\n" + translated.text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", send_movie))
app.add_handler(CommandHandler("translate", translate))
app.add_handler(MessageHandler(filters.Document.ALL, save_file))

app.run_polling()
