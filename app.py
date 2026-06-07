# app.py
import streamlit as st
from database import append_to_sheet
from security import clean_phone_number, validate_name

# إعدادات الواجهة
st.set_page_config(page_title="نظام المبيعات الذكي", page_icon="🎯")
st.title("🎯 نظام المبيعات الاحترافي")

# تهيئة الجلسة
if "step" not in st.session_state: st.session_state.step = "name"
if "temp_name" not in st.session_state: st.session_state.temp_name = ""

# عرض مدخلات المحادثة
user_input = st.chat_input("أدخل البيانات...")

if user_input:
    # --- منطق الخطوات ---
    if st.session_state.step == "name":
        name = validate_name(user_input)
        if name:
            st.session_state.temp_name = name
            st.session_state.step = "phone"
            st.success(f"أهلاً {name}، من فضلك أرسل رقم الهاتف (11 رقم).")
        else:
            st.error("الاسم غير صالح، يرجى إدخال اسم ثلاثي.")

    elif st.session_state.step == "phone":
        phone = clean_phone_number(user_input)
        if phone:
            # هنا سنستدعي دالة الحفظ من ملف database.py
            success = append_to_sheet(st.secrets["SPREADSHEET_ID"], st.session_state.temp_name, phone)
            if success:
                st.balloons()
                st.success("✅ تم حفظ البيانات بنجاح!")
                st.session_state.step = "name" # إعادة الضبط للعميل القادم
            else:
                st.error("حدث خطأ في قاعدة البيانات.")
        else:
            st.error("رقم هاتف غير صحيح! تأكد من إدخال 11 رقماً.")
