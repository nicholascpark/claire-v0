import streamlit as st
from streamlit_chat import message
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

# 1. Vectorise the sales response csv data
loader = CSVLoader(file_path="raw_text_balboa.csv")
documents = loader.load()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)

# 2. Function for similarity search


def retrieve_info(query):
    similar_response = db.similarity_search_with_score(query, k=3)
    
    page_contents_array = [doc[0].page_content for doc in similar_response]
    similarity_scores = [doc[1] for doc in similar_response]
    
    assistant_responses = [item.split('\\nAssistant: ')[1] for item in page_contents_array if '\\nAssistant: ' in item and item.split('\\nAssistant: ')[1]]
    
    return assistant_responses, similarity_scores


llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo-16k-0613")


template = """

You are a highly skilled sales agent and credit counselor specializing in debt consolidation at ClearOne Advantage. 

Your goal is to engage digital prospects on our landing page to qualify them as leads for our program.

{chat_history}

Current Message: {message}

Best Practices: {best_practice}

Guidelines:

Tailor your response to match the assistant of the best practices in length, tone and information.
Ask relevant questions to understand the prospect's financial situation and needs. Avoid repeating questions already asked.
Respond in a natural, conversational manner as if speaking on the phone. Keep responses under 300 characters.
Be concise, empathetic and focus on the prospect's needs and how our debt consolidation program can help their financial future in the long run.

"""

prompt = ChatPromptTemplate(template = template, )

from_template(template=template)
output_parser = StrOutputParser()


# prompt = ChatPromptTemplate(
#     input_variables=["chat_history", "message", "best_practice"],
#     template=template
# )

llm_chain = prompt | llm

# 4. Retrieval augmented generation
def generate_response(message, chat_history, similarity_threshold=0.7):

    # chat_history = chat_history[-5:]

    history_str = "\n".join([f"User: {user_msg}\nAssistant: {assistant_msg}" for user_msg, assistant_msg in chat_history])
    
    best_practice, similarity_scores = retrieve_info(message)
    
    if any(score >= similarity_threshold for score in similarity_scores):
        response = llm_chain.invoke(chat_history=history_str, message=message, best_practice=best_practice)
    else:
        response = llm_chain.invoke(chat_history=history_str, message=message, best_practice="")
    
    return response


def main():
    st.set_page_config(page_title="Customer Response Generator", page_icon=":bird:")
    st.title("Customer Response Generator :bird:")

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    # Initialize the chat_history list
    chat_history = []

    # Container for the chat history
    response_container = st.container()
    # Container for the user's text input
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("You:", key='input', value="")
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = generate_response(user_input, chat_history)
            chat_history.append((user_input, output))
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

if __name__ == '__main__':
    main()