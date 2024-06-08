#############################################################################################################
# Define the prompt template
#############################################################################################################
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from session_manager import get_session_id, create_new_session
from langchain.chains import LLMMathChain, APIChain
from langchain.agents import Tool, load_tools, AgentExecutor, create_openai_tools_agent
from prompts import api_response_prompt, api_url_prompt, main_prompt
from api_docs import leads_api_docs
import os

#############################################################################################################
# Define base model
#############################################################################################################

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = 0, max_tokens = 1000)

#############################################################################################################
# Define the math tool template
#############################################################################################################

llm_math = LLMMathChain(llm=llm)

math_tool = Tool(
    name='Calculator',
    func=llm_math.run,
    description='Useful for when you need to answer questions about math.'
)

#############################################################################################################
# Define the API tool template
#############################################################################################################
                     
# conversation_memory = ConversationBufferMemory(memory_key="chat_history",
#                                                 return_messages=True,
#                                                 max_history_length=10000
#                                                 )

# llm_chain = LLMChain(llm=llm, prompt=main_prompt, memory=conversation_memory)

api_chain = APIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=leads_api_docs,
        api_url_prompt=api_url_prompt,
        api_response_prompt=api_response_prompt,
        verbose=True,
        limit_to_domains=[f"<{os.getenv("CLEARONE_LEADS_API_URL")}>"]
    )

lead_api_tool = Tool(
        name="LeadsHandling",
        description="Leads API tool for lead creation in Salesforce or credit pull of a lead for ClearOne Advantage.",
        func=api_chain.run,
    )

#############################################################################################################
# Define the main prompt template
#############################################################################################################

# tools = [math_tool, lead_api_tool]
tools = [math_tool]
agent = create_openai_tools_agent(llm, tools, main_prompt)
chain = AgentExecutor(agent=agent, tools=tools, verbose=True)

# chain = prompt | llm

def invoke_chain(
        chain_with_message_history, 
        input_message: str, 
        session_id: str = None
    ):

    return chain_with_message_history.invoke(
        input = {"input": input_message},
        config = {"configurable": {"session_id": session_id}}
    )


def collect_chat_history(chain_with_message_history, session_id: str):
    total_chat_str = ' \n'.join(
        [
            x.content for x in chain_with_message_history.get_session_history(session_id).messages
        ]
    )
    return total_chat_str

def collect_latest_chat(chain_with_message_history, session_id: str, n=2):
    latest_chat_str = ' \n'.join(
        [
            x.content for x in chain_with_message_history.get_session_history(session_id).messages[-n:]
        ]
    )
    return latest_chat_str

#############################################################################################################
# Define the Streamlit app
#############################################################################################################

import streamlit as st
from digital_customer import Customer
from extractor import extract_customer_info
import re

def set_streamlit_config():
    st.set_page_config(page_title="ClearOne Advantage AI", page_icon=None, layout="wide")
    st.image('./COA_logo.jpg', caption="Claire v0: AI Assistant for Digital Leads")

def sanitize_output(text):
    return text.replace("*", "").replace("_", "").replace("$", "\$")

def initialize_session_state(USER_ID):
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = create_new_session(USER_ID)
    if 'customer' not in st.session_state:
        st.session_state['customer'] = Customer()
    if 'chain_with_message_history' not in st.session_state:
        message_history = ChatMessageHistory()
        st.session_state['chain_with_message_history'] = RunnableWithMessageHistory(
            chain,
            lambda session_id: message_history,
            input_messages_key="input",
            output_messages_key="output",
            history_messages_key="chat_history",
        )

def generate_intro_message(session_id, chain_with_message_history):
    if not st.session_state['generated']:
        invoke_chain(chain_with_message_history, "", session_id)
        intro_message = chain_with_message_history.get_session_history(session_id).messages[1].content
        st.session_state['past'].append("")
        st.session_state['generated'].append(intro_message)

def display_chat_history(chat_container):
    with chat_container:
        for i, (user_msg, bot_msg) in enumerate(zip(st.session_state['past'], st.session_state['generated'])):
            user_msg = sanitize_output(user_msg)
            if i > 0:
                st.write(f"<span style='color: hotpink;'>**You:**</span> {user_msg}", unsafe_allow_html=True)
            cleaned_bot_msg = sanitize_output(bot_msg)
            # cleaned_bot_msg = bot_msg
            st.write(f"<span style='color: turquoise;'>**Claire:**</span> {cleaned_bot_msg}", unsafe_allow_html=True)

def process_user_input(chain_with_message_history, session_id, user_input, chat_container):
    st.session_state['past'].append(user_input)
    with chat_container:
        st.write(f"<span style='color: hotpink;'>**You:**</span> {user_input}", unsafe_allow_html=True)

    with st.spinner("Claire is typing..."):
        output = invoke_chain(chain_with_message_history, user_input, session_id)
        cleaned_output = sanitize_output(output["output"])
        # cleaned_output = output["output"]
        st.session_state['generated'].append(cleaned_output)

        latest_chat_str = collect_chat_history(chain_with_message_history, session_id)
        new_customer_info = extract_customer_info(latest_chat_str)
        st.session_state['customer'].update_customer_from_string_non_empty(new_customer_info)

        with chat_container:
            st.write(f"<span style='color: turquoise;'>**Claire:**</span> {cleaned_output}", unsafe_allow_html=True)

def main():

    USER_ID = "default_user1"

    set_streamlit_config()

    initialize_session_state(USER_ID)

    session_id = st.session_state['session_id']
    customer = st.session_state['customer']
    chain_with_message_history = st.session_state['chain_with_message_history']

    generate_intro_message(session_id, chain_with_message_history)

    chat_container = st.container()
    display_chat_history(chat_container)

    input_container = st.container()
    with input_container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("You:", key='input', value="")
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            process_user_input(chain_with_message_history, session_id, user_input, chat_container)


if __name__ == "__main__":
    main()
