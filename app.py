import streamlit as st
from database import append_to_sheet
from security import clean_phone_number, validate_name
from notifications import send_telegram_alert
from marketing import get_marketing_message

# إعدادات الواجهة
st.set_page_config(page_title="منظومة المبيعات المتكاملة", page_icon="🎯")
st.title("🎯 نظام المبيعات الاحترافي")

# تهيئة الجلسة
if "step" not in st.session_state: st.session_state.step = "name"
if "temp_name" not in st.session_state: st.session_state.temp_name = ""
if "messages" not in st.session_state: st.session_state.messages = []

# عرض سجل المحادثة للحفاظ على تجربة مستخدم احترافية
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# الترحيب الأولي إذا كانت المحادثة فارغة
if not st.session_state.messages:
    welcome_msg = "أهلاً بك في نظامنا! من فضلك، ابدأ بكتابة اسمك الثلاثي."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    st.rerun()

# استقبال المدخلات
if user_input := st.chat_input("تواصل مع فريق المبيعات..."):
    # عرض مدخلات المستخدم
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
                response = "⚠️ الاسم غير صالح، يرجى إدخال اسم ثلاثي صحيح."

        # 2. مرحلة طلب الهاتف والحفظ
        elif st.session_state.step == "phone":
            phone = clean_phone_number(user_input)
            if phone:
                with st.spinner("جاري حفظ بياناتك في النظام..."):
                    if append_to_sheet(st.session_state.temp_name, phone):
                        # تفعيل التنبيه والتسويق
                        send_telegram_alert(st.session_state.temp_name, phone)
                        offer = get_marketing_message(st.session_state.temp_name)
                        
                        response = f"✅ تم التسجيل بنجاح!\n\n{offer}"
                        st.balloons()
                        st.session_state.step = "name" # إعادة البدء للعميل التالي
                    else:
                        response = "❌ خطأ تقني في الاتصال بقاعدة البيانات."
            else:
                response = "⚠️ رقم غير صحيح، تأكد من إدخال 11 رقماً مصرياً."
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
