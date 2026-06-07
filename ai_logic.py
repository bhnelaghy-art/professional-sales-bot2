import streamlit as st
from groq import Groq

def get_ai_response(user_input, chat_history):
    """إرسال المحادثة لـ Groq للحصول على رد ذكي"""
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # بناء سياق المحادثة
    messages = [{"role": "system", "content": "أنت مساعد مبيعات ذكي ومحترف لشركة قهوة. ردودك قصيرة، ودودة، ومقنعة."}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})

    # استدعاء النموذج
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content
