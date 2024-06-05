import json

leads_api_docs = {
  "base_url": "<https://carbon.clearoneadvantage.com/api/lead/>",
  "endpoints": {
    "/create": {
      "method": "POST",
      "description": "Create a new lead in Salesforce.",
      "parameters": {
        "detailedResponse": {
          "type": "boolean",
          "description": "Set to true for a detailed response."
        },
        "LeadId": {
          "type": "integer",
          "description": "The unique identifier for the lead."
        },
        "Debt": {
          "type": "number",
          "description": "The total debt amount for the lead."
        },
        "FirstName": {
          "type": "string",
          "description": "The lead's first name."
        },
        "LastName": {
          "type": "string",
          "description": "The lead's last name."
        },
        "Address": {
          "type": "string",
          "description": "The lead's address."
        },
        "City": {
          "type": "string",
          "description": "The lead's city."
        },
        "State": {
          "type": "string",
          "description": "The lead's state."
        },
        "Zip": {
          "type": "string",
          "description": "The lead's zip code."
        },
        "Phone": {
          "type": "string",
          "description": "The lead's phone number."
        },
        "DateOfBirth": {
          "type": "string",
          "description": "The lead's date of birth in MM-DD-YYYY format."
        },
        "Email": {
          "type": "string",
          "description": "The lead's email address."
        },
        "LeadSourceId": {
          "type": "string",
          "description": "The identifier for the lead source."
        }
      },
      "response": {
        "description": "A JSON object indicating the result of lead creation.",
        "content_type": "application/json"
      }
    },
    "/affiliate/creditpull": {
      "method": "POST",
      "description": "Perform a credit pull for an affiliate lead.",
      "parameters": {
        "FirstName": {
          "type": "string",
          "description": "The lead's first name."
        },
        "LastName": {
          "type": "string",
          "description": "The lead's last name."
        },
        "SSN": {
          "type": "string",
          "description": "The lead's Social Security Number in XXX-XX-XXXX format."
        },
        "Address": {
          "type": "string",
          "description": "The lead's address."
        },
        "City": {
          "type": "string",
          "description": "The lead's city."
        },
        "State": {
          "type": "string",
          "description": "The lead's state."
        },
        "Zip": {
          "type": "string",
          "description": "The lead's zip code."
        },
        "Phone": {
          "type": "string",
          "description": "The lead's phone number."
        },
        "DateOfBirth": {
          "type": "string",
          "description": "The lead's date of birth in YYYY-MM-DD format."
        },
        "Email": {
          "type": "string",
          "description": "The lead's email address."
        },
        "CheckCreditReportCache": {
          "type": "boolean",
          "description": "Whether to check the credit report cache."
        },
        "LeadRecordId": {
          "type": "string",
          "description": "The Salesforce record ID for the lead."
        },
        "AffiliateName": {
          "type": "string",
          "description": "The name of the affiliate."
        }
      },
      "response": {
        "description": "A JSON object containing credit pull result.",
        "content_type": "application/json"
      }
    }
  }
}

leads_api_docs = json.dumps(leads_api_docs, indent=2)
