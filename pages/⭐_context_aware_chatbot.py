# Import necessary libraries
import utils  # Custom utility functions for handling session state, displaying messages, etc.
import streamlit as st  # Streamlit framework for building interactive web apps
from streaming import StreamHandler  # Custom streaming handler for real-time output
from langchain.prompts import PromptTemplate  # Helps structure chatbot conversation prompts
from langchain.chains import ConversationChain  # Creates a conversation chain with memory
from langchain.memory import ConversationBufferMemory  # Stores conversation history in memory

# Set up Streamlit page configuration
st.set_page_config(page_title="Context Aware Chatbot", page_icon="⭐")

# Display chatbot header and introductory text
st.header('Context Aware Chatbot')
st.write('Enhancing Chatbot Interactions through Context Awareness')

# Display a "View Source Code" badge (linked to GitHub)
st.write('[![view source code](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/MuhammadUmerKhan/LangChain-Chatbots/blob/main/pages/%E2%AD%90_context_aware_chatbot.py)')

class ContextChatbot:
    """A context-aware chatbot that maintains conversation history."""

    def __init__(self):
        """Initialize the chatbot by syncing session state and configuring the LLM."""
        utils.sync_st_session()  # Sync Streamlit session state
        self.llm = utils.configure_llm()  # Configure the language model (LLM)

    @st.cache_resource
    def setup_chain(_self):
        """
        Set up the chatbot's conversation chain with memory and a structured prompt template.
        Cached to avoid unnecessary reinitialization.
        """
        memory = ConversationBufferMemory()  # Initialize memory to store conversation history

        # Define a prompt template to format conversation history properly
        prompt_template = PromptTemplate.from_template(
            "{history}\nHuman: {input}\nAI:"  # Keeps track of past exchanges
        )

        # Create a conversation chain using the language model, memory, and prompt template
        chain = ConversationChain(llm=_self.llm, memory=memory, verbose=False, prompt=prompt_template)
        return chain  # Return the conversation chain object

    @utils.enable_chat_history
    def main(self):
        """
        Main function to handle user input, process responses, and maintain chat history.
        """
        chain = self.setup_chain()  # Initialize the chatbot conversation chain
        
        # Capture user input from Streamlit chat interface
        user_query = st.chat_input(placeholder="Ask me anything!")

        if user_query:  # If the user provides input
            utils.display_msg(user_query, 'user')  # Display the user's message in chat
            
            # Create a chat message container for the assistant's response
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())  # Initialize a streaming response handler
                
                # Generate a response from the chatbot based on user input
                result = chain.invoke(
                    {"input": user_query},  # Provide the user's input
                    {"callbacks": [st_cb]}  # Use callback for streaming response
                )
                
                # Extract the chatbot's response from the result
                response = utils.remove_think_tags(result["response"])

                # Append the chatbot's response to session history (removing "AI:" prefix)
                st.session_state.messages.append({"role": "assistant", "content": response.split("AI:")[-1].strip()})

                # Display the chatbot's response in the chat interface
                st.write(response.split("AI:")[-1].strip())

                # Log the conversation (for debugging or record-keeping)
                utils.print_qa(ContextChatbot, user_query, response)

# Run the chatbot when the script is executed
if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()
