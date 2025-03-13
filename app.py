import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# タイトルとアプリの説明
st.title("専門家AIアシスタント")
st.markdown("""
### アプリの使い方
1. 左のサイドバーから相談したい専門家を選択してください
2. 下の入力フォームに質問を入力してください
3. 送信ボタンをクリックすると、選択した専門家としてAIが回答します
""")

# 専門家の種類と対応するシステムメッセージを定義
expert_types = {
    "プログラミング講師": "あなたはプログラミングの専門家です。初心者にもわかりやすく、技術的な概念を説明してください。コード例を示す場合は、詳細なコメントを付けてください。",
    "栄養士": "あなたは栄養学の専門家です。健康的な食事や栄養バランスについてアドバイスしてください。科学的な根拠に基づいた情報を提供し、一般的な食事の誤解を解くよう努めてください。",
    "金融アドバイザー": "あなたは金融の専門家です。投資、貯蓄、予算管理などについて、わかりやすく実用的なアドバイスを提供してください。専門用語を使う場合は、必ず説明を加えてください。",
    "旅行ガイド": "あなたは旅行の専門家です。世界中の観光地、文化、現地の習慣、おすすめのスポットなどについて詳しく説明してください。旅行者の予算や好みに合わせたアドバイスを心がけてください。"
}

# サイドバーに専門家選択用のラジオボタンを配置
selected_expert = st.sidebar.radio(
    "相談したい専門家を選んでください：",
    list(expert_types.keys())
)

# 選択された専門家に関する説明を表示
st.sidebar.markdown(f"### {selected_expert}に質問します")

# LLMからの回答を取得する関数
def get_ai_response(input_text, expert_type):
    # ChatOpenAIのインスタンスを作成
    chat = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    # システムメッセージを設定（専門家の種類に応じて）
    system_message = SystemMessage(content=expert_types[expert_type])
    
    # ユーザーからの入力をHumanMessageとして設定
    human_message = HumanMessage(content=input_text)
    
    # メッセージのリストを作成
    messages = [system_message, human_message]
    
    # LLMに問い合わせて回答を取得
    response = chat(messages)
    
    return response.content

# 入力フォームと送信ボタン
with st.form(key="question_form"):
    user_input = st.text_area("質問を入力してください：", height=150)
    submit_button = st.form_submit_button("送信")

# 送信ボタンが押されたら回答を表示
if submit_button and user_input:
    with st.spinner("AIが回答を生成中..."):
        ai_response = get_ai_response(user_input, selected_expert)
    
    st.markdown("### 回答:")
    st.markdown(ai_response)
    
    # 会話履歴をセッション状態に保存（オプション）
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.append({
        "expert": selected_expert,
        "question": user_input,
        "answer": ai_response
    })

# 過去の会話履歴を表示（オプション）
if 'history' in st.session_state and len(st.session_state.history) > 0:
    with st.expander("過去の会話履歴", expanded=False):
        for i, exchange in enumerate(st.session_state.history):
            st.markdown(f"**質問 {i+1}** ({exchange['expert']})")
            st.markdown(f"> {exchange['question']}")
            st.markdown(f"**回答 {i+1}**")
            st.markdown(exchange['answer'])
            st.markdown("---")