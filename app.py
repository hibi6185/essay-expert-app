import streamlit as st
import google.generativeai as genai
import PIL.Image

# 1. 페이지 설정 (넓은 화면 모드)
st.set_page_config(page_title="올인원논술", layout="wide")

# 2. API 키 설정 (Secrets 활용)
try:
    api_key = st.secrets["api_key"]
    genai.configure(api_key=api_key)
except:
    st.error("Secrets에 'api_key'가 설정되지 않았습니다.")

# ---------------------------------------------------------
# [강의 데이터 관리함] 
# 나중에 여기에 104개의 제목과 유튜브 링크를 채워 넣으시면 됩니다!
# ---------------------------------------------------------
LECTURES = {
    "기본편 (52강)": {
        "1강: 논술의 시작": "https://www.youtube.com/watch?v=비공개링크1",
        "2강: 문장 만들기": "https://www.youtube.com/watch?v=비공개링크2",
        # ... 여기에 52번까지 추가 가능
    },
    "심화편 (52강)": {
        "1강: 고득점 전략": "https://www.youtube.com/watch?v=비공개링크3",
        "2강: 논리적 추론": "https://www.youtube.com/watch?v=비공개링크4",
        # ... 여기에 52번까지 추가 가능
    }
}

# 3. 메인 탭 생성
tab1, tab2 = st.tabs(["📺 온택트 강의실", "✍️ AI 논술 첨삭"])

# --- [Tab 1: 온택트 강의실] ---
with tab1:
    st.title("📺 온택트 강의실")
    st.write("강의를 시청한 후, 첨삭 탭으로 이동해서 글을 제출하세요.")
    
    col1, col2 = st.columns([1, 3]) # 왼쪽은 선택 메뉴, 오른쪽은 영상
    
    with col1:
        course = st.radio("과정 선택", list(LECTURES.keys()))
        lecture_titles = list(LECTURES[course].keys())
        selected_title = st.selectbox("강의 선택", lecture_titles)
    
    with col2:
        st.subheader(f"🎥 {selected_title}")
        video_url = LECTURES[course][selected_title]
        st.video(video_url)
        st.info("강의를 다 들었다면 상단의 'AI 논술 첨삭' 탭을 클릭하세요!")

# --- [Tab 2: AI 논술 첨삭] ---
with tab2:
    st.title("✍️ AI 논술 첨삭")
    st.write("오늘 배운 내용을 바탕으로 작성한 글을 사진 찍어 올려주세요.")

    uploaded_file = st.file_uploader("논술글 사진을 선택하거나 찍어주세요", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='업로드된 사진', use_container_width=True)
        
        if st.button("전문가 첨삭 시작하기"):
            with st.spinner("선생님이 글을 읽고 계십니다... 잠시만 기다려주세요."):
                try:
                    img = PIL.Image.open(uploaded_file)
                    
                    # 작가님의 6단계 지침을 반영한 프롬프트
                    instruction = """
                    너는 초등 논술 전문가이자 아이들을 사랑하는 다정한 선생님이야. 
                    사진 속 아이의 글을 읽고 다음 6단계 순서에 맞춰 답변해줘:

                    1. [아이의 글 복원]: 사진 속 글자를 그대로 텍스트로 옮겨줘.
                    2. [칭찬 듬뿍]: 아이가 잘 쓴 문장이나 표현을 3가지 찾아 구체적으로 칭찬해줘.
                    3. [더 멋진 표현 제안]: 아쉬운 점은 '이렇게 고쳐보자'라며 다정하게 예시 문장을 보여줘.
                    4. [오늘의 성장 포인트]: 아이의 사고력이 어떻게 발달하고 있는지 전문적으로 분석해줘.
                    5. [부모님께 드리는 팁]: 이 글을 바탕으로 집에서 아이와 어떤 대화를 나누면 좋을지 알려줘.
                    6. [다정한 마무리]: 아이에게 보내는 따뜻한 응원의 메시지로 마쳐줘.

                    말투는 반드시 아이와 엄마가 함께 읽었을 때 행복해지는 다정한 말투(~했구나, ~하렴)를 사용해줘.
                    """
                    
                    model = genai.GenerativeModel('gemini-3.1-flash-lite')
                    response = model.generate_content([instruction, img])
                    
                    st.success("첨삭이 완료되었습니다!")
                    st.markdown("### 📝 첨삭 결과")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
