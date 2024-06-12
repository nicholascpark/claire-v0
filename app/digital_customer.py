from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field

class Customer(BaseModel):
    """Information about a person."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    
    Debt: Optional[str] = Field(
        default=None, description="The total debt of the customer"
    )
    Zip: Optional[str] = Field(
        default=None, description="The zip code of the customer"
    )
    Email: Optional[str] = Field(
        default=None, description="The email address of the customer."
    )
    FirstName: Optional[str] = Field(
        default=None, description="The first name of the customer."
    )
    LastName: Optional[str] = Field(
        default=None, description="The last name of the customer."
    )
    Phone: Optional[str] = Field(
        default=None, description="The phone number of the customer.",
    )
    Address: Optional[str] = Field(
        default=None, description="The street_address of the customer."
    )
    DateOfBirth: Optional[str] = Field(
        default=None, description="The birth date of the customer."
    )
    CreditPullConsent: Optional[str] = Field(
        default=None, description="The credit pull consent of the customer."
    )
    PhoneContactConsent: Optional[str] = Field(
        default=None, description="The phone contact consent of the customer."
    )
    LeadId: Optional[str] = Field(
        default=199, description="The lead id of the customer."
    )

    def update_customer_from_string(self, customer_str: str) -> None:
        # Parse the customer string into a dictionary
        customer_dict = {}
        for field in customer_str.strip().split():
            if '=' in field:
                key, value = field.split('=', 1)
                customer_dict[key.strip()] = value.strip("'")
        
        # Update the current Customer object with the new values
        self.__dict__.update(self.copy(update=customer_dict).__dict__)

    def update_customer_from_string_non_empty(self, customer_str: str) -> None:
        # Parse the customer string into a dictionary
        customer_dict = {}
        for field in customer_str.strip().split():
            if '=' in field:
                key, value = field.split('=', 1)
                if value.strip("'") != "None":
                    customer_dict[key.strip()] = value.strip("'")
        
        # Update the current Customer object with the non-empty fields
        for field, value in customer_dict.items():
            setattr(self, field, value)


    def check_empty_fields(self) -> list:
        ask_for = []
        # Check if fields are empty
        for field, value in self.dict().items():
            if value in [None, "", 0]:  # You can add other 'empty' conditions as per your requirements
                print(f"Field '{field}' is empty.")
                ask_for.append(field)
        return ask_for
    
    def add_customer_info(self, field: str, value: str) -> None:
        setattr(self, field, value)

    def convert_to_json(self) -> dict:
        return self.dict()


def create_customer_from_string(customer_str: str) -> Customer:
    # Parse the customer string into a dictionary
    customer_dict = {}
    for field in customer_str.strip().split():
        if '=' in field:
            key, value = field.split('=', 1)
            customer_dict[key.strip()] = value.strip("'")
    
    # Create a new Customer object from the dictionary
    customer = Customer(**customer_dict)
    return customer


if __name__ == "__main__":
    # Example usage
    user_peronal_details = Customer(
        debt=1000,
        zip_code="12345",
        email="nick@nick.com",
        first_name=None,
        last_name=None,
        phone_number="1234567890",
        street_address="123 Main St",
        birth_date="01/01/1990",
        credit_pull_consent="Yes",
        phone_contact_consent="Yes",
        lead_id = 199
    )   

