# Import necessary libraries
import os
import numpy as np
import streamlit as st
import utils  # ✅ Now using utility functions
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS  # ✅ Use FAISS instead of DocArrayInMemorySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document  # ✅ Needed for FAISS storage

# Set up Streamlit page configuration
st.set_page_config(page_title="Chat with Your Documents", page_icon="📄")

# Display chatbot header
st.header("📄 DocuMind AI: Smart PDF Question Answering System")
st.write("Upload PDFs and ask questions based on their content.")

class CustomDocChatbot:
    """Chatbot for interacting with PDF documents using Retrieval-Augmented Generation (RAG) and FAISS."""

    def __init__(self):
        """Initialize chatbot and load necessary models."""
        utils.sync_st_session()  # ✅ Ensure chat history is synchronized
        self.llm = utils.configure_llm()  # ✅ Load LLM from utils
        self.embedding_model = utils.configure_embedding_model()  # ✅ Load SentenceTransformer from utils
        self.faiss_embeddings = utils.configure_vector_embeddings()  # ✅ Load FAISS-compatible embeddings
    
    def save_file(self, file):
        """Save the uploaded PDF to a temporary folder."""
        folder = "tmp"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        return file_path

    def setup_qa_chain(self, uploaded_files):
        """Processes uploaded PDFs and sets up the Q&A retrieval system with FAISS."""

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
        texts = [doc.page_content for doc in splits]

        # ✅ Generate embeddings manually
        text_embeddings = self.embedding_model.encode(texts)
        text_embeddings = np.array(text_embeddings)  # Convert to numpy array

        # ✅ Convert texts into LangChain Document objects for FAISS
        faiss_docs = [Document(page_content=text) for text in texts]

        # ✅ Initialize FAISS vector store
        vector_db = FAISS.from_documents(faiss_docs, self.faiss_embeddings)

        # Define retriever
        retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})

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

    @utils.enable_chat_history  # ✅ Enable chat history to display previous messages
    def main(self):
        """Main function to handle file uploads and chatbot interactions."""
        uploaded_files = st.sidebar.file_uploader("📤 Upload PDF Files", type=["pdf"], accept_multiple_files=True)

        if not uploaded_files:
            st.error("Please upload PDF documents to continue!")
            st.stop()

        user_query = st.chat_input(placeholder="🔎 Ask something about your document!")

        if uploaded_files and user_query:
            qa_chain = self.setup_qa_chain(uploaded_files)

            utils.display_msg(user_query, "user")  # ✅ Store and display user's message

            with st.chat_message("assistant"):
                result = qa_chain.invoke({"question": user_query})  # Generate response
                response = utils.remove_think_tags(result["answer"])

                st.write(response)  # Show AI response
                st.session_state.messages.append({"role": "assistant", "content": response})  # ✅ Store assistant response

                utils.print_qa(CustomDocChatbot, user_query, response)  # ✅ Log interaction for debugging

# Run the chatbot
if __name__ == "__main__":
    obj = CustomDocChatbot()
    obj.main()
