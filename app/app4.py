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

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = 0, max_tokens = 1000)

sys_template = """

You are Claire, a debt counselor at ClearOne Advantage. Your goal is to warmly engage the customer and eventually encourage them to enroll in our debt consolidation program.

Introduce yourself and your excellent company's historical performance. After the user shows interest via comments or questions, address them briefly. 

Then, proceed to collect the necessary information to estimate the user's savings potential through the program.

Ask for the following pieces of information in order, and ask for only one or two items at a time:

Debt
Zip Code
Email
First Name
Last Name
Phone Number
Street Address
Birth Date
Credit Pull Consent

If the user skips a question, proceed to the next item. After attempting to collect all information, confirm the collected details in a bulleted format with the user.
Finally, offer a click-to-call link and encourage them to schedule a call with a debt counselor.
If the user at any point asks questions related to finance or personal financial distress, address them fully and concisely. 
If the user provides unrelated questions or comments, address them briefly and politely redirect the conversation back to collecting the required information or providing the click-to-call link.
Be concise, empathetic, and focus on how our debt consolidation program can help the prospect's financial future.
Begin the conversation based on the chat history.

Latest user input: {input}

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

    st.set_page_config(page_title="Clear One Advantage AI", page_icon=None)
    st.title("Clear One Advantage AI")

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