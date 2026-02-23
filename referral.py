# referral.py
from db import get_user

def get_ref(user_id):
    """
    Generate referral information for user.
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        str: Referral link and reward info
    """
    try:
        user = get_user(str(user_id))
        if not user:
            return "❌ User not found. Please start with /start"
        
        # user = (id, username, profile)
        username = user[1]
        
        referral_info = f"""
👥 REFERRAL PROGRAM (Coming Soon)
{'='*50}

Your Referral Link:
🔗 https://t.me/YourBotUsername?start={username}

📊 Share & Earn:
• Each referral: +5 credits
• 5 referrals: Free premium plan (1 month)
• 20 referrals: Lifetime premium access
• Leaderboard bonus: Top 10 get special prizes

🎁 Current Rewards:
Your referrals: 0
Credits earned: 0 ⭐

💡 Sharing Tips:
✓ Share in communities
✓ Post on social media
✓ Tell friends about the bot

👉 More rewards coming in PRO version!
"""
        return referral_info
    
    except Exception as e:
        return f"❌ Error fetching referral info: {str(e)}"