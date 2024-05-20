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
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from session_manager import get_session_id, create_new_session

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

sys_template = """

You are an expert debt counselor, specializing in debt consolidation product at ClearOne Advantage.

Given a chat history and the latest user question, your goal is to engage digital prospects on our landing page to qualify them as leads for our program.

Begin by introducing yourself as Claire and collecting the following pieces of information, explaining that you need some info to estimate savings.

Ask for ALL of the following items, one at a time, in this exact order. Proceed to the next item if user skips or avoids answering the question.

Debt
Zip Code
Email
First Name
Last Name
Phone Number
Street Address
Birth Date
Credit Pull Consent

Confirm the information provided by the user after all the questions are asked.

Finally, provide a click-to-call link to the prospect suggesting to schedule a call with a debt counselor.

If there are any unrelated questions or comments at any point, address briefly and politely redirect the user to the information you need to collect to estimate savings or provide a click-to-call link.

Be concise, empathetic and focus on the prospect's needs and how our debt consolidation program can help their financial future in the long run.

Begin:

{input}

"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", sys_template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt | llm

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
from streamlit_chat import message
from digital_customer import Customer
from extractor import extract_customer_info

def main():

    USER_ID = "default_user"

    st.set_page_config(page_title="ClearOne Advantage AI", page_icon=None)
    st.title("ClearOne Advantage AI")

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
            history_messages_key="chat_history",
        )

    session_id = st.session_state['session_id']
    customer = st.session_state['customer']
    chain_with_message_history = st.session_state['chain_with_message_history']

    # Create a container for the chat history
    chat_container = st.container()

    # Create a container for the user's text input
    input_container = st.container()

    with input_container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("You:", key='input', value="")
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = invoke_chain(chain_with_message_history, user_input, session_id)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output.content)

            latest_chat_str = collect_chat_history(chain_with_message_history, session_id)
            new_customer_info = extract_customer_info(latest_chat_str)
            st.session_state['customer'].update_customer_from_string_non_empty(new_customer_info)

    # Display the latest messages in the chat container
    if st.session_state['generated']:
        with chat_container:
            num_messages = len(st.session_state['generated'])
            max_display = 5  # Number of latest messages to display

            for i in range(max(0, num_messages - max_display), num_messages):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style = 'shapes')
                message(st.session_state["generated"][i], key=str(i))
                
if __name__ == "__main__":
    main()