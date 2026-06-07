import streamlit as st
from groq import Groq

def get_ai_response(user_input, chat_history):
    try:
        # التأكد من وجود المفتاح
        if "GROQ_API_KEY" not in st.secrets:
            return "عذراً، لم يتم ضبط مفتاح الـ API في الإعدادات."
            
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        messages = [{"role": "system", "content": "أنت مساعد مبيعات ذكي. ردودك قصيرة ومفيدة."}]
        # تحويل التاريخ لمحاكاة تنسيق الـ API
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192", # جرب استخدام 8b فهو أخف وأسرع وأكثر استقراراً
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # طباعة الخطأ في الـ logs لمعرفة السبب الحقيقي
        print(f"Groq Error: {e}")
        return "عذراً، حدث خطأ تقني في معالجة الطلب. يرجى المحاولة لاحقاً."
