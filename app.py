import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="개발 왕초보 병석이의 소중한 첫 작품(챗봇)",
    page_icon="🤖",
    layout="wide"
)

# API 키 설정 및 모델 초기화
try:
    # secrets.toml에서 API 키 불러오기
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    
    # API 키가 비어있는지 확인
    if not GOOGLE_API_KEY:
        st.error("API 키가 설정되지 않았습니다. .streamlit/secrets.toml 파일에 GOOGLE_API_KEY를 설정해주세요.")
        st.stop()
    
    # Gemini API 구성
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # 모델 초기화
    model = genai.GenerativeModel('gemini-2.0-flash')
    
except Exception as e:
    st.error(f"API 키 설정 중 오류가 발생했습니다: {str(e)}")
    st.error("secrets.toml 파일을 확인해주세요.")
    st.stop()

# 메인 타이틀과 설명
st.title("🤖 개발 왕초보 병석이의 소중한 첫 작품(챗봇)")
st.markdown("Gemini API를 활용한 기본 챗봇 프레임워크입니다.")

# 구분선 추가
st.divider()

# 세션 상태 초기화
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 이전 대화 내용을 보여주는 expander
with st.expander("💬 이전 대화 보기", expanded=False):
    if not st.session_state.chat_history:
        st.info("아직 대화 내역이 없습니다.")
    else:
        for idx, message in enumerate(st.session_state.chat_history):
            # 메시지 스타일 설정
            if message["role"] == "user":
                icon = "👤"
                bg_color = "#f0f2f6"
            else:  # assistant
                icon = "🤖"
                bg_color = "#e8f0fe"
            
            # 메시지 표시
            st.markdown(
                f"""
                <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    <strong>{icon} {'사용자' if message["role"] == "user" else 'Gemini'}:</strong><br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

# 현재 대화 표시
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력해주세요"):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 메시지 히스토리에 사용자 입력 추가
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    try:
        # AI 응답 생성
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            ai_response = response.text
            st.markdown(ai_response)
        
        # AI 응답을 히스토리에 추가
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
    except Exception as e:
        st.error(f"응답 생성 중 오류가 발생했습니다: {str(e)}") 
