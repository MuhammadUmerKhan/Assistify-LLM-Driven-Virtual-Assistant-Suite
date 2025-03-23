# LLM-Driven Intelligent Virtual Assistants

## Introduction
This project consists of three AI-powered chatbots designed using LangChain and Hugging Face models. Each chatbot serves a different purpose, progressively increasing in complexity and functionality. The three chatbots are:

1. **Basic Chatbot** - A simple question-answering bot.
2. **Context-Aware Chatbot** - Retains conversation history for a more interactive experience.
3. **Chat with Your Documents Chatbot** - Allows users to interact with their own documents.

## Features
### 1. Basic Chatbot
- Provides direct answers to user queries.
- Uses a pre-trained LLM (Large Language Model) for responses.
- Ideal for answering general questions.

### 2. Context-Aware Chatbot
- Maintains conversation history for contextual awareness.
- Responds based on previous interactions.
- More interactive and intelligent compared to the basic chatbot.

### 3. Chat with Your Documents Chatbot
- Allows users to upload documents (e.g., PDFs, text files).
- Answers questions based on the document content.
- Uses embeddings to retrieve relevant document sections for responses.

## Setup Instructions
### Prerequisites
- Python 3.10+
- Hugging Face API Key
- Streamlit (for UI)
- Dependencies installed via `pip install -r requirements.txt`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/chatbot-project.git
   cd chatbot-project
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   export HUGGINGFACEHUB_API_TOKEN='your-api-key-here'
   ```

### Running the Chatbots
- **Basic Chatbot**
  ```bash
  streamlit run 💬_BasicChatbot.py
  ```
- **Context-Aware Chatbot**
  ```bash
  streamlit run ⭐_context_aware_chatbot.py
  ```
- **Chat with Your Documents**
  ```bash
  streamlit run 📄_chat_with_your_documents.py
  ```

## Usage
- Open the Streamlit app in your browser.
- Start interacting with the chatbot by typing messages.
- If using the "Chat with Your Documents" bot, upload a document and ask questions based on its content.

## Technologies Used
- **LangChain** for building AI-powered chat applications.
- **Hugging Face Models** for language understanding.
- **FastEmbedEmbeddings** for document-based chatbot search.
- **Streamlit** for an interactive UI.

## Future Improvements
- Add support for more file formats in document-based chatbot.
- Integrate retrieval-augmented generation (RAG) for better document understanding.
- Implement more advanced memory for enhanced context retention.

## Live Demo:
- [Chect out here](https://langhain-chatbots.streamlit.app/)

## Conclusion
This chatbot suite demonstrates different levels of conversational AI, from simple Q&A to context-aware interactions and document-based responses. Feel free to explore and modify the project for further enhancements!

