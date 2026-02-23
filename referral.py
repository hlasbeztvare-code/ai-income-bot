# referral.py
import uuid

def get_ref_code(user_id):
    return f"REF-{user_id}-{uuid.uuid4().hex[:6]}"