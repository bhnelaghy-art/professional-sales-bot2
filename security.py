import re

def clean_phone_number(phone_input):
    """تنظيف رقم الهاتف والتحقق من أنه مصري (11 رقم)"""
    digits = re.sub(r'\D', '', phone_input)
    if len(digits) == 11 and digits.startswith(('010', '011', '012', '015')):
        return digits
    return None

def validate_name(name_input):
    """التحقق من صحة الاسم (على الأقل كلمتين)"""
    name = name_input.strip()
    if len(name.split()) >= 2:
        return name
    return None
