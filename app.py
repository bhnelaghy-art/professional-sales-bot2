import streamlit as st
from database import append_to_sheet
from security import clean_phone_number, validate_name

# إعدادات الواجهة
st.set_page_config(page_title="منظومة المبيعات المتكاملة", page_icon="🎯")
st.title("🎯 نظام المبيعات الاحترافي")

# تهيئة الجلسة
if "step" not in st.session_state: st.session_state.step = "name"
if "temp_name" not in st.session_state: st.session_state.temp_name = ""

# عرض المحادثة
user_input = st.chat_input("تواصل مع فريق المبيعات...")

if user_input:
    # 1. مرحلة طلب الاسم
    if st.session_state.step == "name":
        name = validate_name(user_input)
        if name:
            st.session_state.temp_name = name
            st.session_state.step = "phone"
            st.chat_message("assistant").write(f"أهلاً بك {name}، من فضلك أرسل رقم الهاتف (11 رقماً).")
        else:
            st.error("الاسم غير صالح، يرجى إدخال اسم ثلاثي.")

    # 2. مرحلة طلب الهاتف والحفظ
    elif st.session_state.step == "phone":
        phone = clean_phone_number(user_input)
        if phone:
            with st.spinner("جاري حفظ بياناتك في النظام..."):
                if append_to_sheet(st.session_state.temp_name, phone):
                    st.success("✅ تم التسجيل بنجاح! سنقوم بالتواصل معك قريباً.")
                    st.balloons()
                    st.session_state.step = "name" # إعادة البدء للعميل التالي
                else:
                    st.error("خطأ تقني في الاتصال بقاعدة البيانات.")
        else:
            st.error("رقم غير صحيح، تأكد من إدخال 11 رقماً مصرياً.")
