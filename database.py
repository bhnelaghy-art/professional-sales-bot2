import streamlit as st
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

def get_service():
    creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    return build("sheets", "v4", credentials=creds)

def append_to_sheet(name, phone):
    try:
        service = get_service()
        values = [[name, phone, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]]
        service.spreadsheets().values().append(
            spreadsheetId=st.secrets["SPREADSHEET_ID"], 
            range="Sheet1!A:C", valueInputOption="RAW", 
            body={"values": values}
        ).execute()
        return True
    except:
        return False
