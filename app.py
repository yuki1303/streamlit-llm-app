import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 環境変数からAPIキーを読み込む
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# OpenAI APIキーが設定されていない場合のエラーハンドリングを追加
if not api_key:
    st.error("OpenAI APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。")
    st.stop()

try:
    llm = ChatOpenAI(
        temperature=0.5,
        model="gpt-3.5-turbo",
        api_key=api_key
    )
except Exception as e:
    st.error(f"ChatOpenAIの初期化に失敗しました: {e}")
    st.stop()

# 専門家の種類と対応するシステムメッセージ
types_of_experts = {
    "法律の専門家": "あなたは法律の専門家です。その分野の知識に基づいて回答してください。",
    "動物の専門家": "あなたは動物の専門家です。その分野の知識に基づいて回答してください。"
}

def get_llm_response(user_input: str, expert_type: str) -> str:
    system_prompt = types_of_experts.get(expert_type, "あなたは知識豊富なアシスタントです。")
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"エラーが発生しました: {e}"

# Streamlitアプリ本体
st.title("専門家チャットWebアプリ")
st.write("以下のフォームに相談内容を入力し、専門家に相談することができます。")

st.divider()

# ラジオボタンで専門家選択
expert_type = st.radio("相談したい専門家を選択してください：", ["法律の専門家", "動物の専門家"])

# テキスト入力
user_input = st.text_area("相談内容を入力してください：")

# 実行ボタン
if st.button("送信"):
    st.divider()
    if not user_input.strip():
        st.error("相談内容を入力してください。")
    else:
        with st.spinner('専門家が回答を考えています...'):
            result = get_llm_response(user_input, expert_type)
        st.write("あなたの質問:")
        st.write(user_input)
        st.write("専門家からの回答:")
        st.write(result)