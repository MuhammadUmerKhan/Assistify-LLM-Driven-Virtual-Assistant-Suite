import streamlit as st

# Set the Streamlit page configuration
st.set_page_config(
    page_title="Langchain Chatbot",  # Title displayed on the browser tab
    page_icon='💬',  # Emoji icon for the tab
    layout='wide'  # Use a wide layout for better UI display
)

# Display the main header of the chatbot application
st.header("Chatbot Implementations with Langchain")

# Display GitHub and LinkedIn profile links using badges
st.write("""
[![view source code](https://img.shields.io/badge/GitHub%20Repository-gray?logo=github)](https://github.com/MuhammadUmerKhan/LangChain-Chatbots)
[![linkedin](https://img.shields.io/badge/Muhammad%20Umer-blue?logo=linkedin&color=gray)](https://www.linkedin.com/in/muhammad-umer-khan-61729b260/)
""")

# Introduction to Langchain and chatbot implementations
st.write("""
Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.

Leveraging the power of Langchain, the creation of chatbots becomes effortless. Here are a few examples of chatbot implementations catering to different use cases:

### 🔹 Select a Chatbot to Try:
""")

st.write("""
Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.

Leveraging the power of Langchain, the creation of chatbots becomes effortless. Here are a few examples of chatbot implementations catering to different use cases:

- **Basic Chatbot**: Engage in interactive conversations with the LLM.
- **Chat with your documents**: Empower the chatbot with the ability to access custom documents, enabling it to provide answers to user queries based on the referenced information.
- **Context Aware Chabot**: Empower the chatbot with the ability to access your previous and current chat information.
To explore sample usage of each chatbot, please navigate to the corresponding chatbot section.
""")
