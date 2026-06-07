import re

def clean_phone_number(phone_input):
    """تنظيف الرقم من أي رموز زائدة والتأكد من طوله"""
    # حذف أي شيء ليس رقماً
    digits = re.sub(r'\D', '', phone_input)
    
    # التحقق من أن الرقم مصري (يبدأ بـ 010, 011, 012, 015 وطوله 11)
    if len(digits) == 11 and digits.startswith(('010', '011', '012', '015')):
        return digits
    return None

def validate_name(name_input):
    """التحقق من أن الاسم يحتوي على كلمات حقيقية"""
    # حذف المسافات الزائدة
    name = name_input.strip()
    # التحقق من أن الاسم يتكون من كلمتين على الأقل (اسم ثلاثي مثلاً)
    if len(name.split()) >= 2:
        return name
    return None
