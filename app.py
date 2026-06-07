import streamlit as st
from database import append_to_sheet
from security import clean_phone_number, validate_name
from notifications import send_telegram_alert
from marketing import get_marketing_message
from ai_logic import get_ai_response # استيراد الذكاء الاصطناعي

# إعدادات الواجهة
st.set_page_config(page_title="منظومة المبيعات المتكاملة", page_icon="🎯")
st.title("🎯 نظام المبيعات الاحترافي")

# تهيئة الجلسة
if "step" not in st.session_state: st.session_state.step = "name"
if "temp_name" not in st.session_state: st.session_state.temp_name = ""
if "messages" not in st.session_state: st.session_state.messages = []

# عرض سجل المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# الترحيب الأولي
if not st.session_state.messages:
    welcome_msg = "أهلاً بك في نظامنا! أنا مساعدك الذكي، من فضلك ابدأ بكتابة اسمك الثلاثي."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    st.rerun()

# استقبال المدخلات
if user_input := st.chat_input("تواصل مع فريق المبيعات..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # 1. مرحلة طلب الاسم
        if st.session_state.step == "name":
            name = validate_name(user_input)
            if name:
                st.session_state.temp_name = name
                st.session_state.step = "phone"
                response = f"أهلاً بك {name}، من فضلك أرسل رقم الهاتف (11 رقماً)."
            else:
                # إذا لم يكن اسماً، نستخدم الذكاء الاصطناعي للرد
                response = get_ai_response(user_input, st.session_state.messages[-3:])

        # 2. مرحلة طلب الهاتف والحفظ
        elif st.session_state.step == "phone":
            phone = clean_phone_number(user_input)
            if phone:
                with st.spinner("جاري حفظ بياناتك في النظام..."):
                    if append_to_sheet(st.session_state.temp_name, phone):
                        send_telegram_alert(st.session_state.temp_name, phone)
                        offer = get_marketing_message(st.session_state.temp_name)
                        response = f"✅ تم التسجيل بنجاح!\n\n{offer}"
                        st.balloons()
                        st.session_state.step = "name" 
                    else:
                        response = "❌ خطأ تقني في الاتصال بقاعدة البيانات."
            else:
                # إذا لم يكن رقماً، نسأل الذكاء الاصطناعي للرد أو التوضيح
                response = get_ai_response(user_input, st.session_state.messages[-3:])
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
