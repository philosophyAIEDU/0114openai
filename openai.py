import streamlit as st
import openai

# Streamlit 앱 제목 설정
st.title("OpenAI Assistant 챗봇")

# OpenAI API Key 입력 받기
openai_api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

# OpenAI API Key 설정
openai.api_key = openai_api_key

# Assistant 생성 (한 번만 생성)
if "assistant" not in st.session_state:
    assistant = openai.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview",
    )
    st.session_state.assistant = assistant

# 스레드 ID 초기화
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id

# 사용자 메시지 입력 받기
user_input = st.text_input("메시지를 입력하세요:")

# 메시지 전송 버튼 클릭 시
if st.button("전송"):
    # 사용자 메시지를 스레드에 추가
    message = openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input,
    )

    # Assistant 실행
    run = openai.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=st.session_state.assistant.id,
    )

    # Assistant 응답 대기
    run = openai.beta.threads.runs.retrieve(
        thread_id=st.session_state.thread_id,
        run_id=run.id,
    )
    while run.status == "in_progress":
        run = openai.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id,
        )

    # Assistant 응답 가져오기
    messages = openai.beta.threads.messages.list(
        thread_id=st.session_state.thread_id,
    )
    assistant_message = messages.data[0].content[0].text.value

    # Assistant 응답 출력
    st.write(f"**Assistant:** {assistant_message}")
