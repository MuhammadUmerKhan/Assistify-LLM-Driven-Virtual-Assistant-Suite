import utils
import streamlit as st
from streaming import StreamHandler
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="Context aware chatbot", page_icon="⭐")
st.header('Context aware chatbot')
st.write('Enhancing Chatbot Interactions through Context Awareness')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)]()')

class ContextChatbot:

    def __init__(self):
        utils.sync_st_session()
        self.llm = utils.configure_llm()
    
    @st.cache_resource
    def setup_chain(_self):
        memory = ConversationBufferMemory()
        prompt_template = PromptTemplate.from_template(
            "{history}\nHuman: {input}\nAI:"  # Template structure to include conversation history
        )
        chain = ConversationChain(llm=_self.llm, memory=memory, verbose=False, prompt = prompt_template)
        return chain
    
    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                result = chain.invoke(
                    {"input":user_query},
                    {"callbacks": [st_cb]}
                )
                response = result["response"]
                st.session_state.messages.append({"role": "assistant", "content": response.split("AI:")[-1].strip()})
                st.write(response.split("AI:")[-1].strip())
                # st.write(splitted_response)
                utils.print_qa(ContextChatbot, user_query, response)

if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()