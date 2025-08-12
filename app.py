# 各種ライブラリの読み込み
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()

def get_llm_response(user_message, selected_theme):
    """
    LLMからの回答を取得する処理
    """
    # モデルのオブジェクトを用意
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

    # 選択テーマに応じて使用するプロンプトのシステムメッセージを分岐
    if selected_theme == theme_1:
        system_message = """
            あなたは運動の専門家です。フィットネス、トレーニング、ストレッチ、リハビリテーション、スポーツ科学に関する豊富な知識を持っています。ユーザーの質問には、科学的根拠に基づいた適切なアドバイスを提供し、安全性を最優先に考慮してください。

            あなたの役割は、初心者から上級者まで幅広いユーザーに適した運動方法を提案し、正しいフォームや注意点を指導することです。また、無理な運動を推奨せず、個々の健康状態や目標に応じたアドバイスを行ってください。

            回答には、できるだけ具体的な説明を加え、必要に応じて簡単なステップバイステップのガイドを提供してください。医学的な診断は行わず、健康に不安がある場合は医師の相談を促してください。
        """
    else:
        system_message = """
            あなたは睡眠の専門家です。睡眠科学、睡眠衛生、睡眠障害、リズム管理、リラクゼーション技法に関する深い知識を持っています。ユーザーに対して、科学的根拠に基づいた適切なアドバイスを提供し、健康的な睡眠習慣の確立をサポートしてください。

            あなたの役割は、ユーザーが良質な睡眠を得るための具体的な方法を提案し、睡眠の仕組みや重要性をわかりやすく説明することです。ストレス管理、快適な寝室環境の作り方、規則正しい生活リズムの維持、食事や運動との関係についても適切なアドバイスを行ってください。

            医学的な診断や治療の提案は行わず、重度の睡眠障害が疑われる場合は、専門の医師や睡眠クリニックの受診を推奨してください。

        """
    
    # メッセージリストの用意
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ]
    # LLMからの回答取得
    response = llm(messages)

    return response.content


# 案内文の表示
st.title("運動・睡眠のチャット相談アプリ")
st.write("運動・睡眠に関する生成AIチャット相談アプリです。以下の選択肢から相談したいテーマを選択の上、チャット欄から相談内容を送信すると、専門家AIが的確な回答を行ってくれます。")

# テーマの選択肢を用意
theme_1 = "運動"
theme_2 = "睡眠"

# 相談テーマ選択用のラジオボタン
selected_theme = st.radio(
    "【テーマ】",
    [theme_1, theme_2]
)

# 区切り線
st.divider()

# チャット欄
user_message = st.text_input(label="相談内容を入力してください")

# ボタン
if st.button("送信"):
    # 区切り線
    st.divider()
    # LLMからの回答取得
    response = get_llm_response(user_message, selected_theme)
    # LLMからの回答表示
    st.write(response)