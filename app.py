import streamlit as st
import google.generativeai as genai
from google.cloud import vision
import os

# 1. 구글 서비스 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"
genai.configure(api_key="AIzaSyD0VRot4Wj2YWmUoEL1Lrltm8GhXZau-vk")

# 웹 화면 구성
st.set_page_config(page_title="논술 첨삭 전문가", layout="centered")
st.title("✍️ 다정한 논술 첨삭 선생님")
st.write("아이의 소중한 생각이 담긴 글을 사진으로 올려주세요.")

# 2. 이미지 업로드 레이아웃
uploaded_file = st.file_uploader("논술 이미지를 업로드하세요", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    st.image(uploaded_file, caption='업로드된 이미지', use_container_width=True)
    
    if st.button("전문가 첨삭 시작하기"):
        with st.spinner('아이의 글을 정성껏 읽고 있습니다...'):
            try:
                # [OCR 단계] 글자 추출
                client_vision = vision.ImageAnnotatorClient()
                content = uploaded_file.read()
                image = vision.Image(content=content)
                response = client_vision.text_detection(image=image)
                student_text = response.text_annotations[0].description
                
                st.subheader("📝 인식된 원문")
                st.info(student_text)

                # [AI 첨삭 단계] 
                # 모델 경로 에러를 피하기 위해 풀네임을 사용합니다.
                model = genai.GenerativeModel('gemini-3.1-flash-lite')
                
                # 작가님의 최신 [지침] 반영
                prompt = f"""
                너는 아이들의 잠재력을 끌어내는 따뜻한 글쓰기 선생님이자 논술 전문가야. 
                아래 [지침]을 엄격히 준수하여 학생의 글을 첨삭해줘.

                [지침]
                1. 학생의 독특한 말투와 창의적인 생각은 최대한 살릴 것. (어른스러운 문체로 억지로 바꾸지 말 것)
                2. 맞춤법과 띄어쓰기는 완벽하게 교정할 것.
                3. '제목-서론-본론-결론'의 구조가 부족하다면 구조를 잡아주는 조언을 해줄 것.
                4. 문장 사이 흐름이 어색하면 적절한 접속사를 추천할 것.
                5. 원문에 제목이 있는지 확인해서 먼저 적어주고, 추가로 '창의적인 제목 후보 1개'와 '글 내용 짐작 가능하게 하는 제목 1개'를 제안할 것.
                6. 학생이 자신감을 얻도록 칭찬으로 시작해서 따뜻하게 마무리할 것.

                학생의 글: 
                {student_text}
                """

                result = model.generate_content(prompt)
                
                st.subheader("🌟 전문가 첨삭 결과")
                st.success(result.text)
                
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다. (상세내용: {e})")