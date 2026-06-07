import streamlit as st
# استيراد الوحدات (كل وحدة تمثل قطاع من الـ 1000 ميزة)
from database import append_to_sheet, get_db_data
from security import clean_phone_number, validate_name
from notifications import send_telegram_alert
from marketing import apply_discount_logic
from ai_logic import analyze_intent

# إعدادات الواجهة
st.set_page_config(page_title="منظومة 1000 ميزة", layout="wide")

def main():
    st.title("🚀 النظام المؤسسي المتكامل")
    
    # تهيئة الحالة
    if "step" not in st.session_state: st.session_state.step = "name"
    
    # 1. طبقة الذكاء (AI Analysis)
    user_input = st.chat_input("تواصل مع النظام...")
    if user_input:
        intent = analyze_intent(user_input) # تحليل النية (ميزة ذكاء)
        
        # 2. طبقة الحوار (Logic Flow)
        if st.session_state.step == "name":
            name = validate_name(user_input)
            if name:
                st.session_state.temp_name = name
                st.session_state.step = "phone"
                st.write("تم حفظ الاسم. أرسل رقم الهاتف:")
            else:
                st.error("الاسم غير صالح.")
        
        elif st.session_state.step == "phone":
            phone = clean_phone_number(user_input)
            if phone:
                # 3. طبقة التنفيذ (Execution)
                if append_to_sheet(st.secrets["SPREADSHEET_ID"], st.session_state.temp_name, phone):
                    send_telegram_alert(st.session_state.temp_name, phone) # إشعار
                    discount = apply_discount_logic() # ميزة تسويقية
                    st.success(f"تم التسجيل! كود الخصم الخاص بك: {discount}")
                    st.session_state.step = "name"
            else:
                st.error("رقم غير صحيح.")

if __name__ == "__main__":
    main()
