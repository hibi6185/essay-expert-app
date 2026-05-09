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
                    너는 초중등 논술 전문가이자 아이들의 창의적인 아이디어를 확대해주는 논술 선생님이야. 모두가 똑같은 정답이나 모범답안만을 요구하지 않고, 학생의 번뜩이는 아이디어와 창의성 및 어조를 최대한 살려주면서 창의적이고 가독성 좋은 글을 쓸 수 있게 가이드해주려는 교육철학을 갖고 있어.
                    사진 속 아이의 글을 읽고 아래의 가이드라인에 맞춰 답변해줘:

                    1. [나의 글]: 사진 속 글자를 그대로 텍스트로 옮겨줘.
                    2. [잘한 부분]: 아이가 잘 쓴 문장이나 표현을 3가지 찾아 구체적으로 크게 칭찬해줘. (너무 길지는 않게)
                    3. [제목은 이렇게!]: 아이가 쓴 제목이 '글의 주제를 담은 창의적 제목' 또는 '쓴 글의 내용을 짐작할 수 있는 요약적 제목'인지 확인하고 아니라면 이러한 제목을 2개 추천해줘.
                    4. [이렇게 고치면 더 좋아요!]: 제목-서론-본론-결론 구조가 있는지 확인하기, 글의 주제에 맞는지 적합성 확인하기, 내용이 일관적인지 확인하기, 맞춤법과 띄워쓰기 교정하기.
                    5. [응원메세지]: 아이에게 보내는 따뜻한 응원의 메시지로 마쳐줘.

                    말투는 반드시 아이와 엄마가 함께 읽었을 때 행복해지는 다정한 말투이면서도 존댓말을 사용해줘.
                    """
                    
                    model = genai.GenerativeModel('gemini-3.1-flash-lite')
                    response = model.generate_content([instruction, img])
                    
                    st.success("첨삭이 완료되었습니다!")
                    st.markdown("### 📝 첨삭 결과")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
