# Import necessary libraries
import os  # For file handling and directory creation
import utils  # Custom utility functions for session handling, model configuration, etc.
import streamlit as st  # Streamlit framework for interactive web apps
from streaming import StreamHandler  # Custom streaming handler for real-time response output

# LangChain components
from langchain.memory import ConversationBufferMemory  # Stores chat history for contextual conversation
from langchain.chains import ConversationalRetrievalChain  # Combines retrieval-based document search with conversational AI
from langchain_community.document_loaders import PyPDFLoader  # Loads PDF files into text format
from langchain_community.vectorstores import DocArrayInMemorySearch  # In-memory vector store for document retrieval
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Splits large documents into smaller chunks

# Set up Streamlit page configuration
st.set_page_config(page_title="ChatPDF", page_icon="📄")

# Display chatbot header and description
st.header('Chat with your documents (Basic RAG)')
st.write('Has access to custom documents and can respond to user queries by referring to the content within those documents')

# Display a "View Source Code" badge with a GitHub link
st.write('[![view source code](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/MuhammadUmerKhan/LangChain-Chatbots/blob/main/pages/%F0%9F%93%84_chat_with_your_documents.py)')

class CustomDocChatbot:
    """A chatbot that enables users to ask questions about uploaded PDF documents using Retrieval-Augmented Generation (RAG)."""

    def __init__(self):
        """Initialize the chatbot by syncing session state and configuring the models."""
        utils.sync_st_session()  # Sync Streamlit session state
        self.llm = utils.configure_llm()  # Configure the Language Model (LLM)
        self.embedding_model = utils.configure_embedding_model()  # Configure the embedding model for vector storage

    def save_file(self, file):
        """
        Save the uploaded file to a temporary folder.

        Args:
            file: Uploaded file object.

        Returns:
            file_path (str): Path to the saved file.
        """
        folder = 'tmp'  # Temporary folder to store uploaded PDFs
        if not os.path.exists(folder):  # Create folder if it doesn't exist
            os.makedirs(folder)

        file_path = f'./{folder}/{file.name}'  # Construct file path
        with open(file_path, 'wb') as f:  # Open file in write-binary mode
            f.write(file.getvalue())  # Write file contents
        return file_path  # Return file path

    @st.spinner('Analyzing documents..')
    def setup_qa_chain(self, uploaded_files):
        """
        Set up the Question-Answering (QA) chain by processing the uploaded documents.

        Args:
            uploaded_files: List of uploaded PDF files.

        Returns:
            qa_chain: ConversationalRetrievalChain for question answering.
        """
        # Load and process documents
        docs = []
        for file in uploaded_files:
            file_path = self.save_file(file)  # Save file locally
            loader = PyPDFLoader(file_path)  # Load the PDF
            docs.extend(loader.load())  # Extract text from the PDF and store it

        # Split documents into smaller chunks for better retrieval
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Each chunk will have ~1000 characters
            chunk_overlap=200  # Overlapping region to preserve context between chunks
        )
        splits = text_splitter.split_documents(docs)  # Split the extracted documents

        # Store document chunks in an in-memory vector database for similarity search
        vectordb = DocArrayInMemorySearch.from_documents(splits, self.embedding_model)

        # Define the retriever to search for relevant document chunks
        retriever = vectordb.as_retriever(
            search_type='mmr',  # Maximum Marginal Relevance (MMR) search for diversity
            search_kwargs={'k': 2, 'fetch_k': 4}  # Fetch top 4 results but return 2 most relevant ones
        )

        # Set up memory to store previous conversations for context
        memory = ConversationBufferMemory(
            memory_key='chat_history',  # Key to store chat history
            output_key='answer',  # Key for storing responses
            return_messages=True  # Keep messages in memory
        )

        # Create a Conversational QA chain combining LLM, retriever, and memory
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,  # Use the configured LLM
            retriever=retriever,  # Use the retriever to find relevant document chunks
            memory=memory,  # Include conversation history
            return_source_documents=True,  # Return source documents for reference
            verbose=False  # Suppress unnecessary logs
        )
        return qa_chain  # Return the QA chain instance

    @utils.enable_chat_history
    def main(self):
        """
        Main function to handle file uploads, user queries, and chatbot responses.
        """

        # Sidebar for file uploads
        uploaded_files = st.sidebar.file_uploader(
            label='Upload PDF files',
            type=['pdf'],  # Restrict to PDF files only
            accept_multiple_files=True  # Allow multiple file uploads
        )

        # Stop execution if no files are uploaded
        if not uploaded_files:
            st.error("Please upload PDF documents to continue!")  # Display error message
            st.stop()  # Stop further execution

        # Capture user query input
        user_query = st.chat_input(placeholder="Ask me anything!")

        if uploaded_files and user_query:  # Proceed if user uploaded files and entered a query
            qa_chain = self.setup_qa_chain(uploaded_files)  # Set up the QA chain

            utils.display_msg(user_query, 'user')  # Display user's query

            # Create a chat message container for the assistant's response
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())  # Initialize a streaming response handler

                # Generate a response from the chatbot based on user query
                result = qa_chain.invoke(
                    {"question": user_query},  # Pass user query to the QA system
                    {"callbacks": [st_cb]}  # Use callback for streaming response
                )

                # Extract chatbot response
                response = result["answer"]

                # Append the chatbot's response to session history
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Log the conversation for debugging or record-keeping
                utils.print_qa(CustomDocChatbot, user_query, response)

                # Display references for the extracted response
                for idx, doc in enumerate(result['source_documents'], 1):
                    filename = os.path.basename(doc.metadata['source'])  # Extract filename from metadata
                    page_num = doc.metadata['page']  # Extract page number from metadata
                    ref_title = f":blue[Reference {idx}: *{filename} - page.{page_num}*]"  # Format reference title

                    # Display reference content in a popover
                    with st.popover(ref_title):
                        st.caption(doc.page_content)  # Show document content snippet

# Run the chatbot when the script is executed
if __name__ == "__main__":
    obj = CustomDocChatbot()
    obj.main()
