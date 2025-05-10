# Import required libraries
import os  # Used for environment variable access
import streamlit as st  # Streamlit for building UI
from datetime import datetime  # Used for logging timestamps
from streamlit.logger import get_logger  # Streamlit's built-in logger
from sentence_transformers import SentenceTransformer  # Embeddings
from langchain.embeddings import HuggingFaceEmbeddings  # Open-source embeddings
from langchain_groq import ChatGroq  # Groq API for LLM
from langchain_openai import ChatOpenAI  # OpenAI API for LLM
from dotenv import load_dotenv
load_dotenv()  # ✅ Load environment variables from .env

# Initialize logger for tracking interactions and errors
logger = get_logger("LangChain-Chatbot")

# ✅ API Key Handling (For Local & Deployed Environments)
grok_api_key = os.getenv("GROK_API_KEY")  # Langchain Groq API key (Generate from: https://console.groq.com/)

# Check if API key is available
api_token = grok_api_key
if not api_token:
    st.error("❌ Missing API Token!")
    st.stop()  # Stop execution if API token is missing

# ✅ Decorator to enable chat history
def enable_chat_history(func):
    """
    Decorator to handle chat history and UI interactions.
    Ensures chat messages persist across interactions.
    """
    current_page = func.__qualname__  # Get function name to track current chatbot session

    # Clear session state if model/chatbot is switched
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page  # Store the current chatbot session
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()  # Clear cached resources
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except Exception:
            pass  # Ignore errors if session state keys do not exist

    # Initialize chat history if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Display chat history in the UI
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)  # Execute the decorated function

    return execute

def display_msg(msg, author):
    """
    Displays a chat message in the UI and appends it to session history.

    Args:
        msg (str): The message content to display.
        author (str): The author of the message ("user" or "assistant").
    """
    st.session_state.messages.append({"role": author, "content": msg})  # Store message in session
    st.chat_message(author).write(msg)  # Display message in Streamlit UI

def configure_llm():
    """
        Configure LLM to run on Hugging Face Inference API (Cloud-Based).
        
        Returns:
            llm (LangChain LLM object): Configured model instance.
    """
    
    available_llms = {
        "Qwen": "qwen-qwq-32b",
        "Llama 3": "llama-3.3-70b-versatile",
        "Gemma": "gemma2-9b-it",
        "DeepSeek": "deepseek-r1-distill-llama-70b",
        "Llama 4": "meta-llama/llama-4-scout-17b-16e-instruct",
        "GPT-4": "gpt-4"
    }

    # Sidebar dropdown
    llm_opt = st.sidebar.selectbox("🤖 **Select an LLM Model**", list(available_llms.keys()), key="llm_select")
    model_id = available_llms[llm_opt]

    if model_id == "gpt-4":
        openai_key = st.sidebar.text_input("🔐 Enter OpenAI API Key", type="password", key="OPENAI_API_KEY_INPUT")
        if not openai_key:
            st.error("❌ Please enter your OpenAI API Key!")
            st.stop()
        llm = ChatOpenAI(
            model_name="gpt-4",
            api_key=openai_key,
            temperature=0.3,
            metadata={"model_name": llm_opt}
        )
    else:
        llm = ChatGroq(model_name=model_id, temperature=0.3, groq_api_key=grok_api_key)

    # Display active model
    st.sidebar.success(f"✅ Active Model: {llm_opt}")
    return llm

def print_qa(cls, question, answer):
    """
    Logs the Q&A interaction for debugging and tracking.

    Args:
        cls (class): The calling class.
        question (str): User question.
        answer (str): Model response.
    """
    log_str = f"\nUsecase: {cls.__name__}\nQuestion: {question}\nAnswer: {answer}\n" + "-" * 50
    logger.info(log_str)  # Log the interaction using Streamlit's logger

@st.cache_resource  # Cache the embedding model to avoid reloading it every time
def configure_embedding_model():
    """
    Configures and caches the embedding model.

    Returns:
        embedding_model (FastEmbedEmbeddings): The loaded embedding model.
    """
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # Load and return the embedding model

@st.cache_resource
def configure_vector_embeddings():
    """
    Configures and caches the vector embeddings for Groq API.

    Returns:
        vector_embeddings (HuggingFaceEmbeddings): The loaded vector embeddings.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # Load and return the vector embeddings

def sync_st_session():
    """
    Ensures Streamlit session state values are properly synchronized.
    """
    for k, v in st.session_state.items():
        st.session_state[k] = v  # Sync all session state values