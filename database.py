import streamlit as st
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# إعدادات الخدمة (تُقرأ مرة واحدة فقط)
def get_service():
    try:
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        creds = Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        return build("sheets", "v4", credentials=creds)
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return None

def append_to_sheet(spreadsheet_id, name, phone):
    service = get_service()
    if not service: return False
    
    try:
        values = [[name, phone, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]]
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, 
            range="Sheet1!A:C", # تأكد أن اسم الشيت هو Sheet1
            valueInputOption="RAW", 
            body={"values": values}
        ).execute()
        return True
    except Exception:
        return False
