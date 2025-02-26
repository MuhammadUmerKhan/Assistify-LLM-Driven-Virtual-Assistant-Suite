# Import necessary modules
import utils  # Custom utility functions for chatbot configuration and message handling
import streamlit as st  # Streamlit for building the chatbot UI
from streaming import StreamHandler  # Custom streaming handler for real-time response updates
from langchain.chains import ConversationChain  # Conversation model from LangChain for handling chat history
from langchain.prompts import PromptTemplate  # LangChain's prompt template for structuring conversation inputs

# Set up the Streamlit UI
st.set_page_config(page_title="LLM Chatbot", page_icon="💬")  # Set the page title and icon
st.header("Basic Chatbot")  # Display the chatbot title
st.write("Allows users to interact with LLMs.")  # Display chatbot description
st.write('[![View Source Code](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/MuhammadUmerKhan/LangChain-Chatbots/blob/main/pages/%F0%9F%92%AC_BasicChatbot.py)')  # Display a button linking to source code

class BasicChatBot:
    def __init__(self):
        """Initialize the chatbot by configuring the LLM model."""
        self.llm = utils.configure_llm()  # Configure the LLM model (e.g., OpenAI, Llama)

    def setup_chain(self):
        """Sets up the conversation chain with a custom prompt template."""
        prompt_template = PromptTemplate.from_template(
            "{history}\nHuman: {input}\nAI:"  # Template structure to include conversation history
        )
        return ConversationChain(
            llm=self.llm,  # Use the configured LLM model
            prompt=prompt_template,  # Use the custom prompt template
            verbose=False  # Disable verbose logging
        )

    @utils.enable_chat_history  # Decorator to enable chat history handling
    def main(self):
        """Main function to handle user interaction with the chatbot."""
        chain = self.setup_chain()  # Initialize the conversation chain
        user_query = st.chat_input(placeholder="Ask me anything!")  # Capture user input in chat format

        if user_query:  # If user enters a query
            utils.display_msg(user_query, 'user')  # Display the user's message in chat history

            with st.chat_message("assistant"):  # Display assistant's response in the chat UI
                st_sb = StreamHandler(st.empty())  # Create a streaming handler for real-time response display
                result = chain.invoke(
                    {"input": user_query},  # Pass user input to the LLM
                    {"callbacks": [st_sb]}  # Register the streaming callback
                )
                response = result["response"]  # Extract chatbot response
                
                # Extract only the AI-generated response (remove unnecessary text)
                # splitted_response = response.split("AI:")[1].strip()  

                # Store the assistant's response in the session state
                st.session_state.messages.append({"role": "assistant", "content": response})  

                # Display the cleaned AI response
                st.write(response)

                # Log the interaction for debugging or analytics
                utils.print_qa(BasicChatBot, user_query, response)

# Run the chatbot application when script is executed
if __name__ == "__main__":
    obj = BasicChatBot()  # Create an instance of the chatbot class
    obj.main()  # Run the chatbot's main function
