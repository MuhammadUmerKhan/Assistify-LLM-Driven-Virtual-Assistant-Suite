# Import necessary libraries
import os
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer  # ✅ Correct embedding model
from langchain_groq import ChatGroq  # ✅ Import Groq API for LLM
from dotenv import load_dotenv
load_dotenv()

# ✅ Load API key for LLM
grok_api_key = os.getenv("GROK_API_KEY")

# ✅ Define LLM separately without utils.py
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=grok_api_key,
    model_name="llama-3.3-70b-versatile"  # Set your model name
)

# Set up Streamlit page configuration
st.set_page_config(page_title="Chat with Your Documents", page_icon="📄")

# Display chatbot header
st.header("📄 Chat with Your Documents")
st.write("Upload PDFs and ask questions based on their content.")

class CustomDocChatbot:
    """Chatbot for interacting with PDF documents using Retrieval-Augmented Generation (RAG)."""

    def __init__(self):
        """Initialize chatbot and load necessary models."""
        self.llm = llm  # ✅ Directly use LLM without utils.py
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # ✅ Load embedding model

    def save_file(self, file):
        """Save the uploaded PDF to a temporary folder."""
        folder = "tmp"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        return file_path

    def setup_qa_chain(self, uploaded_files):
        """Processes uploaded PDFs and sets up the Q&A retrieval system."""

        # Load and process documents
        docs = []
        for file in uploaded_files:
            file_path = self.save_file(file)
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())

        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Extract raw text from chunks
        text_chunks = [doc.page_content for doc in splits]

        # ✅ Generate embeddings manually
        text_embeddings = self.embedding_model.encode(text_chunks)

        # ✅ Use `from_texts()` to correctly initialize `DocArrayInMemorySearch`
        vectordb = DocArrayInMemorySearch.from_texts(text_chunks, embedding=self.embedding_model)

        # Define retriever
        retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})

        # Set up memory
        memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True)

        # Create Q&A Chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=False
        )
        return qa_chain

    def main(self):
        """Main function to handle file uploads and chatbot interactions."""
        uploaded_files = st.sidebar.file_uploader("📤 Upload PDF Files", type=["pdf"], accept_multiple_files=True)

        if not uploaded_files:
            st.error("Please upload PDF documents to continue!")
            st.stop()

        user_query = st.chat_input(placeholder="🔎 Ask something about your document!")

        if uploaded_files and user_query:
            qa_chain = self.setup_qa_chain(uploaded_files)

            st.chat_message("user").write(user_query)  # Display user query

            with st.chat_message("assistant"):
                result = qa_chain.invoke({"question": user_query})  # Generate response
                response = result["answer"]

                st.write(response)  # Show AI response
                st.session_state.messages.append({"role": "assistant", "content": response})  # Store response

# Run the chatbot
if __name__ == "__main__":
    obj = CustomDocChatbot()
    obj.main()
