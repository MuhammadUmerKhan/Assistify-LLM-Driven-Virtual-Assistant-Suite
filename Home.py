import streamlit as st

# Set the Streamlit page configuration
st.set_page_config(
    page_title="Langchain Chatbot",
    page_icon='💬',
    layout='wide'
)

# Inject CSS
st.markdown("""
    <style>
        /* Enhanced Dark Theme for Chatbot Application */
        .stApp {
            background: linear-gradient(rgba(31, 41, 55, 0.9), rgba(31, 41, 55, 0.9)), url('https://kriyatec.com/wp-content/uploads/2020/05/chatbot2.jpeg');
            background-size: cover;
            background-attachment: fixed;
            color: #e5e7eb;
            font-family: 'Inter', sans-serif;
        }
        .main-container {
            background: linear-gradient(135deg, rgba(45, 55, 72, 0.85), rgba(30, 58, 138, 0.85));
            border-radius: 12px;
            padding: 25px;
            margin: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
            border: 2px solid #f59e0b;
            backdrop-filter: blur(8px);
        }
        .main-title {
            font-size: 2.8em;
            font-weight: 700;
            color: #4f46e5;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 0 0 10px rgba(79, 70, 229, 0.8);
            animation: pulseGlow 2s ease-in-out infinite;
        }
        .section-title {
            font-size: 2em;
            font-weight: 600;
            color: #4f46e5;
            margin: 30px 0 15px;
            text-shadow: 0 0 8px rgba(79, 70, 229, 0.8);
            border-left: 5px solid #4f46e5;
            padding-left: 15px;
            animation: slideInLeft 0.5s ease-in-out;
        }
        .content {
            font-size: 1.1em;
            color: #e5e7eb;
            line-height: 1.8;
            text-align: justify;
        }
        .highlight {
            color: #f59e0b;
            font-weight: 600;
        }
        .separator {
            height: 2px;
            background: linear-gradient(to right, #4f46e5, #10b981);
            margin: 20px 0;
        }
        .stButton>button {
            background: linear-gradient(45deg, #4f46e5, #10b981);
            color: #e5e7eb;
            border-radius: 10px;
            padding: 12px 25px;
            font-weight: 600;
            font-size: 1em;
            border: none;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.8);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #4338ca, #059669);
            box-shadow: 0 0 20px rgba(245, 158, 11, 1);
            transform: scale(1.05);
            color: #ffffff;
        }
        .stButton>button::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 300%;
            height: 300%;
            background: rgba(245, 158, 11, 0.2);
            transition: all 0.5s ease;
            transform: translate(-50%, -50%) scale(0);
            border-radius: 50%;
        }
        .stButton>button:hover::after {
            transform: translate(-50%, -50%) scale(1);
        }
        .stChatInput, .stTextInput, .stFileUploader {
            background: linear-gradient(135deg, rgba(45, 55, 72, 0.9), rgba(30, 58, 138, 0.9));
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #f59e0b;
            color: #e5e7eb;
            transition: all 0.3s ease;
        }
        .stChatInput:hover, .stTextInput:hover, .stFileUploader:hover {
            border-color: #f59e0b;
            box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
        }
        .stChatInput label, .stTextInput label, .stFileUploader label {
            color: #f59e0b;
            font-weight: 500;
        }
        .stChatMessage.user {
            background: rgba(79, 70, 229, 0.2);
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #4f46e5;
        }
        .stChatMessage.assistant {
            background: rgba(16, 185, 129, 0.2);
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #10b981;
        }
        .footer {
            font-size: 0.9em;
            color: #e5e7eb;
            margin-top: 40px;
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, rgba(45, 55, 72, 0.85), rgba(30, 58, 138, 0.85));
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border: 2px solid #f59e0b;
            backdrop-filter: blur(8px);
        }
        .footer a {
            color: #f59e0b;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }
        .footer a:hover {
            color: #4f46e5;
            text-decoration: underline;
        }
        .content ul li::marker {
            color: #f59e0b;
        }
        .error-text {
            color: #ef4444;
            font-weight: 600;
            text-align: center;
        }
        @keyframes pulseGlow {
            0% { text-shadow: 0 0 8px rgba(79, 70, 229, 0.8); }
            50% { text-shadow: 0 0 16px rgba(79, 70, 229, 1); }
            100% { text-shadow: 0 0 8px rgba(79, 70, 229, 0.8); }
        }
        @keyframes slideInLeft {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes scaleIn {
            from { transform: scale(0.95); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# Display the main header of the chatbot application
st.markdown('<div class="main-title">Chatbot Implementations with Langchain</div>', unsafe_allow_html=True)

# Wrap content in main-container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Display GitHub and LinkedIn profile links using badges
st.markdown("""
    <div class="content">
        <a href="https://github.com/MuhammadUmerKhan/LangChain-Chatbots" target="_blank">
            <img src="https://img.shields.io/badge/GitHub%20Repository-gray?logo=github&color=%234f46e5" alt="view source code">
        </a>
        <a href="https://www.linkedin.com/in/muhammad-umer-khan-61729b260/" target="_blank">
            <img src="https://img.shields.io/badge/Muhammad%20Umer-blue?logo=linkedin&color=%23f59e0b" alt="linkedin">
        </a>
    </div>
""", unsafe_allow_html=True)

# Introduction to Langchain and chatbot implementations
st.markdown("""
    <div class="content">
        Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.
    </div>
    <div class="section-title">🔹 Select a Chatbot to Try:</div>
    <div class="content">
        Leveraging the power of Langchain, the creation of chatbots becomes effortless. Here are a few examples of chatbot implementations catering to different use cases:
        <ul>
            <li><span class="highlight">Basic Chatbot</span>: Engage in interactive conversations with the LLM.</li>
            <li><span class="highlight">Chat with your documents</span>: Empower the chatbot with the ability to access custom documents, enabling it to provide answers to user queries based on the referenced information.</li>
            <li><span class="highlight">Context Aware Chatbot</span>: Empower the chatbot with the ability to access your previous and current chat information.</li>
        </ul>
        To explore sample usage of each chatbot, please navigate to the corresponding chatbot section.
    </div>
""", unsafe_allow_html=True)

# Close main-container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Developed by <a href="https://www.linkedin.com/in/muhammad-umer-khan-61729b260/" target="_blank">Muhammad Umer Khan</a>. Powered by Langchain. 🧠
    </div>
""", unsafe_allow_html=True)