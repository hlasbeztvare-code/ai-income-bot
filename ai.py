from telegram.ext import Application, CommandHandler

async def start(update, ctx):
    await update.message.reply_text("GROK MODE ACTIVATED 🚀 Co chceš vydělat?")

app = Application.builder().token("TG_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()

def build_plan_prompt(goal:str, time_per_day:str, budget:str) -> str:
    return f"""
Jsi AI kouč pro online příjem. Vrať stručně a akčně:
1) 1 nejlepší model pro uživatele
2) 30denní plán po týdnech
3) "DNES udělej" (max 3 kroky)
4) Doporučené legální nástroje (bez slibů jistého zisku)
Profil:
- cíl: {goal}
- čas/den: {time_per_day}
- rozpočet: {budget}
Piš česky, jasně, krátké odrážky.
""".strip()