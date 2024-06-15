import json

leads_api_docs = """
BASE URL: https://carbon.clearoneadvantage.com/api/lead/

The API endpoint /create?detailedResponse=true accepts the following parameters:

Method: POST
Description: Create a new lead in Salesforce.

Parameters:
1. LeadId (integer, required): Always 197. The unique identifier for the lead.
2. Debt (number, required): The total debt amount for the lead.
3. FirstName (string, required): The lead's first name.
4. LastName (string, required): The lead's last name.
5. Address (string, required): The lead's address.
6. City (string, required): The lead's city.
7. State (string, required): The lead's state.
8. Zip (string, required): The lead's zip code.
9. Phone (string, required): The lead's phone number.
10. DateOfBirth (string, required): The lead's date of birth in MM-DD-YYYY format.
11. Email (string, Optional): The lead's email address.

Response:
Description: A JSON object indicating the result of lead creation.
Content-Type: application/json

Example of a successful response:
{
    "Data": {
        "RecordId": "00QUd0000091NQRMA2",
        "IsDuplicate": false
    },
    "Success": true,
    "Message": "Created Salesforce lead 00QUd0000091NQRMA2 (numeric ID -2018134)",
    "Errors": []
}
"""

# leads_api_docs = {
#   "base_url": "<https://carbon.clearoneadvantage.com/api/lead/>",
#   "endpoints": {
#     "/create?detailedResponse=true": {
#       "method": "POST",
#       "description": "Create a new lead in Salesforce.",
#       "parameters": {
#         "LeadId": {
#           "type": "integer",
#           "description": "Always 197. The unique identifier for the lead."
#         },
#         "Debt": {
#           "type": "number",
#           "description": "The total debt amount for the lead."
#         },
#         "FirstName": {
#           "type": "string",
#           "description": "The lead's first name."
#         },
#         "LastName": {
#           "type": "string",
#           "description": "The lead's last name."
#         },
#         "Address": {
#           "type": "string",
#           "description": "The lead's address."
#         },
#         "City": {
#           "type": "string",
#           "description": "The lead's city."
#         },
#         "State": {
#           "type": "string",
#           "description": "The lead's state."
#         },
#         "Zip": {
#           "type": "string",
#           "description": "The lead's zip code."
#         },
#         "Phone": {
#           "type": "string",
#           "description": "The lead's phone number."
#         },
#         "DateOfBirth": {
#           "type": "string",
#           "description": "The lead's date of birth in MM-DD-YYYY format."
#         },
#         "Email": {
#           "type": "string",
#           "description": "The lead's email address."
#         }
#       },
#       "response": {
#         "description": "A JSON object indicating the result of lead creation.",
#         "content_type": "application/json"
#       }
#     },
#     "/affiliate/creditpull": {
#       "method": "POST",
#       "description": "Perform a credit pull for an affiliate lead.",
#       "parameters": {
#         "FirstName": {
#           "type": "string",
#           "description": "The lead's first name."
#         },
#         "LastName": {
#           "type": "string",
#           "description": "The lead's last name."
#         },
#         "SSN": {
#           "type": "string",
#           "description": "The lead's Social Security Number in XXX-XX-XXXX format."
#         },
#         "Address": {
#           "type": "string",
#           "description": "The lead's address."
#         },
#         "City": {
#           "type": "string",
#           "description": "The lead's city."
#         },
#         "State": {
#           "type": "string",
#           "description": "The lead's state."
#         },
#         "Zip": {
#           "type": "string",
#           "description": "The lead's zip code."
#         },
#         "Phone": {
#           "type": "string",
#           "description": "The lead's phone number."
#         },
#         "DateOfBirth": {
#           "type": "string",
#           "description": "The lead's date of birth in YYYY-MM-DD format."
#         },
#         "Email": {
#           "type": "string",
#           "description": "The lead's email address."
#         },
#         "CheckCreditReportCache": {
#           "type": "boolean",
#           "description": "Whether to check the credit report cache."
#         },
#         "LeadRecordId": {
#           "type": "string",
#           "description": "The Salesforce record ID for the lead."
#         },
#         "AffiliateName": {
#           "type": "string",
#           "description": "The name of the affiliate."
#         }
#       },
#       "response": {
#         "description": "A JSON object containing credit pull result.",
#         "content_type": "application/json"
#       }
#     }
#   }
# }

# leads_api_docs = json.dumps(leads_api_docs, indent=2)
