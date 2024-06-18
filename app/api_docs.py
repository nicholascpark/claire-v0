import json

lead_create_api_docs = """
BASE URL: https://carbon.clearoneadvantage.com/api/lead/

The API endpoint /create?detailedResponse=true accepts the following parameters:

Method: POST
Description: Create a new lead in Salesforce.

Parameters:
1. LeadId (integer, required): Always 197. The unique identifier for the lead.
2. Debt (number, required): The total debt amount for the lead.
3. FirstName (string, required): The lead's first name.
4. LastName (string, required): The lead's last name.
5. Address (string, Optional): The lead's address.
6. Zip (string, required): The lead's zip code.
7. Phone (string, required): The lead's phone number.
8. DateOfBirth (string, Optional): The lead's date of birth in MM-DD-YYYY format.
9. Email (string, required): The lead's email address.
10. City (string, required): The lead's city.
11. State (string, Optional): The lead's state.

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

credit_pull_api_docs = """
BASE URL: https://carbon.clearoneadvantage.com/api/affiliate/creditpull

The API endpoint accepts the following parameters:

Method: POST
Description: Pull credit information for a prospect.

Parameters:
1. FirstName (string, required): Prospect's first name.
2. LastName (string, required): Prospect's last name.
3. SSN (string, required): Social Security Number. Either SSN or Address and DOB need to be provided for Credit Pull.
4. Address (string, required): Prospect's address.
5. City (string, required): City name.
6. State (string, required): Two-letter state code.
7. Zip (string, required): 5- or 9-digit zip code.
8. Phone (string, Optional): Prospect's phone number.
9. DateOfBirth (string, required): Prospect's date of birth in YYYY-MM-DD format.
10. Email (string, Optional): Prospect's email address.
11. CheckCreditReportCache (boolean, Optional): Checks COA’s database if a credit report already exists. Default is False.
12. LeadRecordId (string, Optional): COA’s identifier for lead.
13. AffiliateName (string, Optional): Name of the affiliate company.

Response:
Description: A JSON object indicating the result of the credit pull.
Content-Type: application/json

Example of a successful response:
{
    "Data": {
        "CreditPullId": "VKMJ84RD80UODxVmjo8KTRco7p07rmcUYgGB5O75hoqpgiyHZddw3V3iALPO39vfRB1OZwFrFd58l8Bn8t6HLKU5qwkAPFskGIO80UmJJkTl16QFyttMKONeEr5icvM8",
        "SearchRequestId": 0,
        "SearchResultId": 0,
        "LeadRecordId": "-230735",
        "DatePulled": "2023-06-29T13:38:51.491",
        "CreditBureauProcessor": "Experian",
        "InformationalMessages": [],
        "TotalEligibleDebt": 6373.0,
        "AvgDaysDelinquentEligibleDebt": 0
    },
    "Success": true,
    "Errors": []
}

Example of a 400 error response:
{
    "Success": false,
    "Errors": [
        "The Address field is required.",
        "The Zip field is required."
    ]
}

There are also times where the credit pull will provide results of NO-HIT (Equifax) and No Record Found (Experian):
{
    "Data": {
        "CreditPullId": "VKMJ84RD80UODxVmjo8KTRco7p07rmcUYgGB5O75hoqpgiyHZddw3V3iALPO39vfRB1OZwFrFd58l8Bn8t6HLKU5qwkAPFskGIO80UmJJkTl16QFyttMKONeEr5icvM8",
        "SearchRequestId": 0,
        "SearchResultId": 0,
        "DatePulled": "0001-01-01T00:00:00-05:00",
        "CreditBureauProcessor": "Equifax",
        "InformationalMessages": []
    },
    "Success": false,
    "Errors": [
        "Experian - Please verify the client demographic info and re-try the pull after editing the fields in the credit pull page if there are corrections.",
        "Equifax - NO-HIT"
    ]
}
"""