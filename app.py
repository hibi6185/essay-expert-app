import streamlit as st
import google.generativeai as genai

# 1. Secrets에서 API 키 가져오기
try:
    api_key = st.secrets["api_key"]
    genai.configure(api_key=api_key)
except:
    st.error("Secrets에 'api_key'가 설정되지 않았습니다.")

st.title("✍️ 다정한 논술 선생님")
st.write("아이의 글을 사진으로 찍어 올려주세요. 정성껏 첨삭해 드립니다.")

# 2. 이미지 업로드 기능
uploaded_file = st.file_uploader("논술글 사진을 선택하거나 찍어주세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    st.image(uploaded_file, caption='업로드된 사진', use_container_width=True)
    
    if st.button("전문가 첨삭 시작하기"):
        with st.spinner("선생님이 글을 읽고 계십니다... 잠시만 기다려주세요."):
            try:
                # 이미지를 읽어서 Gemini에게 전달
                import PIL.Image
                img = PIL.Image.open(uploaded_file)
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([
                    "너는 초등 논술 전문가이자 다정한 선생님이야. 이 사진 속 아이의 글을 읽고 텍스트로 추출한 뒤, 다정한 말투로 칭찬과 개선점을 첨삭해줘.", 
                    img
                ])
                
                st.success("첨삭이 완료되었습니다!")
                st.markdown("### 📝 첨삭 결과")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"첨삭 중 오류가 발생했습니다: {e}")
