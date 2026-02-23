from telegram.ext import Application, CommandHandler
from ai_router import get_plan
from referral import get_ref

TOKEN = "TG_TOKEN"

async def start(update, ctx):
    await update.message.reply_text("⚡ AI MONEY BOT ONLINE")

async def plan(update, ctx):
    await update.message.reply_text(get_plan(update.message.from_user.id))

async def ref(update, ctx):
    await update.message.reply_text(get_ref(update.message.from_user.id))

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan))
    app.add_handler(CommandHandler("ref", ref))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())