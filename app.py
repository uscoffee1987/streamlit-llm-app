import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain import LLMChain

from dotenv import load_dotenv
load_dotenv()

# -----ここからUIを書く------
st.title("各専門家が質問に回答するアプリ")
st.write("専門家に質問を投げかけると、それぞれの専門家が回答します。")

selected_expert = st.radio(
    "専門家を選んでください",
    ["医師", "弁護士", "エンジニア"]
)
st.divider()

st.text_input("質問を入力してください", key="question")

# -----ここからロジックを書く------

template = """
あなたは{expert}です。以下の質問に対して、専門的な知識を活かして回答してください。

{question}

"""

prompt = PromptTemplate(
    input_variables=["expert", "question"],
    template=template
)

llm = ChatOpenAI(model_name="gpt-4o-mini",temperature=0.5)
chain = LLMChain(llm=llm, prompt=prompt)

if st.button("質問する"):
    question = st.session_state.get("question", "")
    if not question.strip():
        st.error("質問を入力してください。")
    else:
        response = chain.run({
            "expert": selected_expert,
            "question": question
        })
        st.write("回答:")
        st.write(response)