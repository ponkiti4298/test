import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io


# セッション状態の初期化関数
def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

# ユーザーメッセージを追加する関数
def add_user_message(content):
    st.session_state.messages.append({"role": "user", "content": content})

# アシスタントメッセージを追加する関数
def add_assistant_message(content):
    st.session_state.messages.append({"role": "assistant", "content": content})

# チャットメッセージを表示する関数
def display_chat():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"**ユーザー:** {message['content']}")
        else:
            st.write(f"**アシスタント:** {message['content']}")

# ファイルをBase64エンコードする関数
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Streamlitアプリのタイトルを設定する
st.title("説明ボット")

# セッション状態の初期化
initialize_session_state()

# これまでのメッセージを表示
display_chat()

# 画像ファイルのアップロードウィジェットを表示
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 画像を表示
    st.image(uploaded_file, caption='アップロードされた画像', use_column_width=True)

    # 画像をBase64形式にエンコード
    base64_image = encode_image(uploaded_file)

    # ユーザーメッセージを追加
    add_user_message("この画像は何を意味していますか?")

    # Chat Completions APIを呼び出す
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "この画像は何を意味していますか?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ]
    )

    # アシスタントメッセージを追加
    add_assistant_message(response.choices[0].message.content)

    # チャットメッセージを再表示
    display_chat()

# ユーザーが新しいメッセージを入力できるテキストボックス
if prompt := st.chat_input("質問やメッセージを入力してください"):
    # ユーザーメッセージを追加
    add_user_message(prompt)

    # Chat Completions APIを呼び出す
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=st.session_state.messages
    )

    # アシスタントメッセージを追加
    add_assistant_message(response.choices[0].message.content)

    # チャットメッセージを再表示
    display_chat()