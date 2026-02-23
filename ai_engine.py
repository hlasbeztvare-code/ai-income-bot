# ai_engine.py
import openai

PERSONA = """
You are GROK MODE: brutal, practical, concise money coach.
Give actionable steps only.
"""

def generate_plan(level):
    prompt = f"{PERSONA}\nCreate money plan for {level}."
    # fake output placeholder
    return "DAY1: Create offer. DAY2: Post on TikTok. DAY3: Sell."