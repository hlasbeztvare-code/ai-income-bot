import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from db import init_db, upsert_user, set_profile, get_user, log_event
from ai_router import get_plan
from referral import get_ref

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME", "YOURBOT")

STATE = {}  # Simple state management for MVP

GOALS = ["💰 Přivýdělek (rychle)", "🚀 Rozjet projekt", "📱 Monetizovat publikum"]
TIMES = ["15 min/den", "30 min/den", "60+ min/den"]
BUDGETS = ["0 Kč", "do 500 Kč", "500–2000 Kč", "2000+ Kč"]

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    init_db()
    tg_id = str(update.effective_user.id)
    ref = ctx.args[0] if ctx.args else "none"
    upsert_user(tg_id, ref)
    log_event(tg_id, f"start_referral:{ref}")

    kb = [[InlineKeyboardButton("⚡ Začít (30 s)", callback_data="onb_goal")]]
    await update.message.reply_text("INCOME PILOT AI 🚀\nUděláme ti plán do 30 sekund.", reply_markup=InlineKeyboardMarkup(kb))

async def onb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    tg_id = str(q.from_user.id)

    if q.data == "onb_goal":
        kb = [[InlineKeyboardButton(g, callback_data=f"goal|{g}")] for g in GOALS]
        await q.message.reply_text("1/3 Co chceš?", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data.startswith("goal|"):
        goal = q.data.split("|", 1)[1]
        STATE[tg_id] = {"goal": goal}
        kb = [[InlineKeyboardButton(t, callback_data=f"time|{t}")] for t in TIMES]
        await q.message.reply_text("2/3 Kolik času denně?", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data.startswith("time|"):
        time_per_day = q.data.split("|", 1)[1]
        STATE.setdefault(tg_id, {})["time_per_day"] = time_per_day
        kb = [[InlineKeyboardButton(b, callback_data=f"budget|{b}")] for b in BUDGETS]
        await q.message.reply_text("3/3 Rozpočet na nástroje?", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data.startswith("budget|"):
        budget = q.data.split("|", 1)[1]
        profile = STATE.get(tg_id, {})
        goal = profile.get("goal", "")
        time_per_day = profile.get("time_per_day", "")
        set_profile(tg_id, goal, time_per_day, budget)
        log_event(tg_id, f"onboard_complete:{goal}|{time_per_day}|{budget}")

        kb = [
            [InlineKeyboardButton("🧠 Vygeneruj plán", callback_data="plan")],
            [InlineKeyboardButton("👥 Pozvi kámoše", callback_data="ref")]
        ]
        await q.message.reply_text("Hotovo ✅\nChceš plán hned?", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data == "ref":
        link = f"https://t.me/{BOT_USERNAME}?start={tg_id}"
        ref_text = get_ref(tg_id)
        await q.message.reply_text(ref_text)

    elif q.data == "plan":
        plan = get_plan(tg_id)
        await q.message.reply_text(plan)
        log_event(tg_id, "plan_requested")

async def plan_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    tg_id = str(update.effective_user.id)
    log_event(tg_id, "plan_cmd")
    plan = get_plan(tg_id)
    await update.message.reply_text(plan)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan_cmd))
    app.add_handler(CallbackQueryHandler(onb))
    app.run_polling()

if __name__ == "__main__":
    main()