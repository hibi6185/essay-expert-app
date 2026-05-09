import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account

# Streamlit Secrets에서 정보를 가져와 인증 정보(Credentials)를 만듭니다.
# 작가님이 Secrets에 넣으신 정보를 딕셔너리 형태로 변환합니다.
info = {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    "universe_domain": st.secrets["universe_domain"]
}

# 서비스 계정 인증 정보를 생성합니다.
credentials = service_account.Credentials.from_service_account_info(info)

# Vision API와 Gemini 설정에 이 인증 정보를 사용합니다.
# (이 부분은 작가님의 기존 코드 흐름에 맞춰 genai를 설정하는 부분입니다.)
# API 키가 필요하다면 Secrets에 따로 api_key를 추가하거나, 
# 위 credentials를 활용하도록 코드를 다듬어야 합니다.
