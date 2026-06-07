import requests
import streamlit as st

def send_telegram_alert(name, phone):
    """إرسال تنبيه فوري لتليجرام"""
    token = st.secrets["TELEGRAM_TOKEN"]
    chat_id = st.secrets["TELEGRAM_CHAT_ID"]
    message = f"🎯 عميل جديد!\nالاسم: {name}\nالرقم: {phone}\nالوقت: الآن"
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.get(url, params={"chat_id": chat_id, "text": message})
    except:
        pass # إذا فشل التنبيه لا نوقف النظام
