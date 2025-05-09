# 🚀 LLM-Driven Intelligent Virtual Assistants

## 🌟 Introduction
Welcome to this exciting project featuring three AI-powered chatbots built with **LangChain** and a variety of advanced language models! These chatbots cater to diverse needs, ranging from simple conversations to context-aware interactions and document-based queries. Here's a quick overview:

- **💬 Basic Chatbot**: A straightforward Q&A bot for general queries.
- **⭐ Context-Aware Chatbot**: Remembers past interactions for smarter conversations.
- **📄 Chat with Your Documents Chatbot**: Answers questions based on your uploaded documents.

## 🎉 Features
### 1. 💬 Basic Chatbot
- Delivers quick, direct responses to user questions.
- Powered by pre-trained LLMs for reliable answers.
- Perfect for casual or exploratory chats! 🎯

### 2. ⭐ Context-Aware Chatbot
- Maintains a history of your conversation for context.
- Offers intelligent, personalized replies based on past inputs.
- Elevates the chatting experience with memory! 🧠

### 3. 📄 Chat with Your Documents Chatbot
- Lets you upload documents (e.g., PDFs, text files) for analysis.
- Provides answers by retrieving relevant document sections.
- Utilizes embeddings for accurate, document-specific responses. 📚

## 🛠️ Setup Instructions
### ✅ Prerequisites
- Python 3.10+ 🐍
- API Keys: Hugging Face, Groq, or OpenAI (depending on model selection)
- Streamlit for a sleek UI 🌐
- Install dependencies with `pip install -r requirements.txt`

### 🚀 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/chatbot-project.git
   cd chatbot-project
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (e.g., in a `.env` file):
   ```
   HUGGINGFACEHUB_API_TOKEN=your-hf-api-key
   GROK_API_KEY=your-grok-api-key
   OPENAI_API_KEY=your-openai-api-key
   ```

### 🎮 Running the Chatbots
- **💬 Basic Chatbot**:
  ```bash
  streamlit run 💬_BasicChatbot.py
  ```
- **⭐ Context-Aware Chatbot**:
  ```bash
  streamlit run ⭐_context_aware_chatbot.py
  ```
- **📄 Chat with Your Documents**:
  ```bash
  streamlit run 📄_chat_with_your_documents.py
  ```

## 🎤 Usage
- Launch the Streamlit app in your browser.
- Start chatting by typing your messages! 💬
- For the 📄 Chatbot, upload a document and ask questions related to its content. 📝

## 💻 Technologies Used
- **LangChain**: Framework for building AI chat applications. 🛠️
- **Models**: Llama 3, Gemma, Qwen, DeepSeek, Llama 4, GPT-4 (configurable via sidebar). 🤖
- **FastEmbedEmbeddings**: Enhances document search capabilities. 🔍
- **Streamlit**: Creates an interactive, user-friendly interface. 🌐

## 🌱 Future Improvements
- Support additional file formats (e.g., Word, Excel) for the document chatbot. 📊
- Integrate retrieval-augmented generation (RAG) for deeper document insights. 🔎
- Enhance memory features for even smarter context retention. 🧠

## 🌐 Live Demo
- [Check it out here](https://langchain-chatbots.streamlit.app/?embed_options=dark_theme) 🌟

## 🎯 Conclusion
This chatbot suite showcases the power of conversational AI, from basic Q&A to context-aware and document-based interactions. Dive in, experiment, and feel free to enhance it further! 🚀
