import random
import string

def generate_discount_code():
    """توليد كود خصم عشوائي فريد"""
    return "SAVE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

def get_marketing_message(name):
    """صياغة رسالة تسويقية مخصصة"""
    code = generate_discount_code()
    return f"شكراً يا {name}! استخدم كود الخصم **{code}** في طلبك القادم للحصول على 20% خصم."
