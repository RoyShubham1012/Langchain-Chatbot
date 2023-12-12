from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *

st.subheader("Adaptive Question Chatbot")

if 'buffer_memory' not in globals():
   buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

    # print("x")

if 'responses' not in globals():
    responses = ["How can I assist you?"]

if 'requests' not in globals():
    requests = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", openai_api_key="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")



system_msg_template = SystemMessagePromptTemplate.from_template(
    template="Answer the question as truthfully as possible. If the answer is not in the text below, say 'I don't know'"
)

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# container for chat history
response_container = st.container()
# container for text box
text_container = st.container()

with text_container:
    query = st.text_input("You: ", key="input")
    print('rrgr', st.session_state)
    if query:
        with st.spinner("Typing..."):
            response = conversation.predict(input=query)
        requests.append(query)
        responses.append(response)

with response_container:
    if responses:
        for i, response_text in enumerate(responses):
            message(response_text, key=f"response_{i}")
            if i < len(requests):
                message(requests[i], is_user=True, key=f"user_input_{i}")
