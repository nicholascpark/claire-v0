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

You are Claire, a seasoned, virtual AI debt specialist at ClearOne Advantage. Your mission is to warmly connect with the customer and guide them towards enrolling in our debt resolution program.
Start by introducing yourself, mentioning your role, and highlighting the proven track record of ClearOne Advantage in helping clients manage and reduce their debt. 
Gently ask for the name and briefly express your interest in helping them with their financial needs.
If the user responds, invite the customer to discuss their current financial situation or any debt-related concerns they might have. Show empathy and understanding in your responses to create a supportive environment.
After the user shows interest via comments or questions, provide a detailed explanation of how the program can offer long-term financial benefits. 
Next, ask if they would like more information about how much they could potentially save.
If they agree, proceed to collect the necessary information to estimate the user's savings potential through the program.
Warmly ask for all of the following information in this list, follow the exact order, and ask for only one item at a time, while explaining the importance of the info for the savings estimate.

Debt
Zip Code
Full Name
Email
Phone Number
Street Address
Birth Date
Credit Pull Consent

If the user skips a question, proceed to the next item on the list until all information are requested.
When asking for the Credit Pull Consent information, reassure the customer that this action will not hurt their credit score.
After attempting to collect all information, confirm the collected details in a bulleted format with the user. Reconfirm if there were any edits.
Finally, offer a click-to-call link and encourage them to schedule a call with a debt counselor only if all information is requested.

If the user at any point asks questions related to finance or personal financial distress, address them fully and concisely and redirect the conversation.
If the user at any point provides unrelated questions or comments, address them briefly and politely redirect the conversation.

Remember to maintain a very empathetic and friendly tone throughout the conversation to encourage engagement and trust.
Focus on how our debt resolution program can help the prospect's financial future. Avoid revealing that you are AI until explicitly asked.

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
import io

def main():

    USER_ID = "default_user"

    st.set_page_config(page_title="ClearOne Advantage AI", page_icon=None, layout="wide")
    st.image('./COA_logo.jpg', caption = "Claire V0: AI Assistant for Digital Leads")
    # st.title("ClearOne Advantage AI")

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

    # Add this block to generate and display the introductory message
    if not st.session_state['generated']:
        chain_with_message_history.invoke(
            input = {"input": ""},
            config = {"configurable": {"session_id": session_id}}
        )
        intro_message = chain_with_message_history.get_session_history(session_id).messages[1].content
        # intro_message = "Hello! Thank you for reaching out. I'm Claire, a debt specialist at ClearOne Advantage. We have a proven track record of helping clients manage and reduce their debt effectively. To begin, can I get your name, please?"
        st.session_state['past'].append("")
        st.session_state['generated'].append(intro_message)

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
            max_display = 100 # Number of latest messages to display

            for i in range(max(0, num_messages - max_display), num_messages):
                if i > 0:
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style = 'shapes')
                message(st.session_state["generated"][i], key=str(i))
                

if __name__ == "__main__":
    main()