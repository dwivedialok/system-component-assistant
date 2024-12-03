import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplate import css, user_template, bot_template
import base64

CONFIG_FILE_PATH = '.7ytrepmnt'
OPEN_AI_MODEL_NAME = "gpt-4o-mini"
QDRANT_COLL_NAME = "github_issues_coll"
GITHUB_REPO_ISSUES_LINK = "https://github.com/spring-projects/spring-boot/issues"


def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"


# Use this function to get the base64 string
base64_image_dev = get_image_base64("chat_dev.png")
base64_image_robo = get_image_base64("chat_robo.png")


def get_qdrant_client():
    qdrant_url = os.getenv("QDRANT_HOST_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    return QdrantClient(
        url=qdrant_url,
        # api_key=qdrant_api_key,
    )


def get_existing_vector_store(collection_identity):

    qdrant_client = get_qdrant_client()

    embeddings = OpenAIEmbeddings()
    return Qdrant(
        client=qdrant_client,
        collection_name=collection_identity,
        embeddings=embeddings,
    )


def get_conversation_chain():
    llm = ChatOpenAI(model_name=OPEN_AI_MODEL_NAME, temperature=0,verbose=True)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    qdrant = get_existing_vector_store(QDRANT_COLL_NAME)
    retriever = qdrant.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        verbose=True
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content).replace("{{IMG}}", base64_image_dev), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content).replace("{{IMG}}", base64_image_robo), unsafe_allow_html=True)


def main():

    # Load all needed environment variables
    load_dotenv(CONFIG_FILE_PATH)
    st.set_page_config(page_title="Q&A assistant for Github Issues", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with Github Issues :books:")

    with st.sidebar:
        st.subheader("Connecting to Github Issues for Q&A")
        st.write(f"Github Repo Issues Link: {GITHUB_REPO_ISSUES_LINK}")
        st.session_state.conversation = get_conversation_chain()
        st.subheader("Successfully connected to Github Issues for Q&A")
        st.write("This app uses an LLM Model to answer questions related to problems discussed in configured Github "
                 "Issues.")

    user_question = st.text_input("Ask a question related to Github Issues:")
    if user_question:
        handle_userinput(user_question)


if __name__ == '__main__':
    main()
