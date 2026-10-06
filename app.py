from data.students import generate_student_data
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import logging
import os
from assistant import Assistant
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
from langchain_openai import ChatOpenAI
from gui import AssistantGUI


if __name__ == "__main__":

    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    st.set_page_config(page_title="TIT Agartala Assistant", page_icon="🎓", layout="wide")

    @st.cache_data(ttl=3600, show_spinner="Loading Student Data...")
    def get_user_data():
        return generate_student_data(1)[0]

    @st.cache_resource(ttl=3600, show_spinner="Loading Vector Store...")
    def init_vector_store(pdf_path):
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000, chunk_overlap=200
            )
            splits = text_splitter.split_documents(docs)

            embedding_function = HuggingFaceEmbeddings(
             model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            persistent_path = "./data/vectorstore"

            vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embedding_function,
    persist_directory=persistent_path,
)

            return vectorstore
        except Exception as e:
            logging.error(f"Error initializing vector store: {str(e)}")
            st.error(f"Failed to initialize vector store: {str(e)}")
            return None

    user_data = get_user_data()
    vector_store = init_vector_store("data/tit_agartala_policies.pdf")

    if "user" not in st.session_state:
        st.session_state.user = user_data
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": WELCOME_MESSAGE}]

        

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        user_information=st.session_state.user,
        vector_store=vector_store,
    )

gui = AssistantGUI(assistant)
gui.render()
