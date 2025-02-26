# This transform classifies a user as "Internal" or "External" based on their email domain.
#   - If the email domain is "company.com", the user is classified as "Internal".
#   - Otherwise, the user is classified as "External".


from isc_transform_generator import *

# Collecting the User's Email
email = identityAttribute("email")

# Extracting the Email Domain
domain = split(delimiter="@", index=1, input=email)

# Condition to Classify User as Internal or External
classification = conditional(
    expression="$domain eq company.com",
    positive_condition=static("Interno"),
    negative_condition=static("Externo"),
    domain=domain
)

# Generate the transform
transform("User Classification", classification)


# RESULT:
'''
{
    "name": "User Classification",
    "attributes": {
        "expression": "$domain eq company.com",
        "positiveCondition": {
            "attributes": {
                "value": "Interno"
            },
            "type": "static"
        },
        "negativeCondition": {
            "attributes": {
                "value": "Externo"
            },
            "type": "static"
        },
        "domain": {
            "type": "split",
            "attributes": {
                "delimiter": "@",
                "index": 1,
                "input": {
                    "attributes": {
                        "name": "email"
                    },
                    "type": "identityAttribute"
                },
                "throws": true
            }
        }
    },
    "type": "conditional"
}
'''
