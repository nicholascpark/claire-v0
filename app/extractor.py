from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from digital_customer import Customer

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        ("human", "{text}"),
    ]
)

from langchain_openai import ChatOpenAI

extracting_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
structured_llm = extracting_model.with_structured_output(Customer) | prompt

def extract_customer_info(text: str):
    extracted_info = structured_llm.invoke(text)
    return extracted_info.messages[1].content


if __name__ == "__main__":

    # Example usage
    text = """
    Hello\nI'm a debt counselor specializing in debt consolidation at ClearOne Advantage. To better assist you, may I ask for some information to estimate potential savings for you? \n\nCould you please provide me with the total amount of debt you have?\nI have 7200 in debt\nThank you for sharing that. \n\nCould you please provide me with your zip code?\n07928\nGreat, thank you. \n\nWhat is the best email to reach you at?\nnick@nick.com\nThank you for providing your email. \n\nMay I have your first name, last name, and phone number to better assist you with our debt consolidation program?\nNick Park\nThank you, Nick. \n\nMay I have your phone number and street address to continue assisting you with our debt consolidation program?\n2017484848\nThank you, Nick. \n\nMay I have your street address to proceed with assisting you with our debt consolidation program?\n72 bell ave, 12/12/1990\nThank you, Nick. I have all the information I need to estimate potential savings for you. \n\nWould you also be willing to provide consent for a credit pull as part of our assessment process?\n\nFinally, if you're ready to take the next step, you can schedule a call with one of our debt counselors by clicking the link below:\n\n[Schedule a Call](tel:8881234567)
    """
    extracted_info = extract_customer_info(text)
    print(extracted_info)

    