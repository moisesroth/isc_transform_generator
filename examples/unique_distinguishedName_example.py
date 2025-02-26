# Example result for a ser with name "John Doe"
#   CN=J.Doe,OU=Users,DC=YourDomain,DC=com
#   CN=John.Doe,OU=Users,DC=YourDomain,DC=com
#   CN=John..Doe1,OU=Users,DC=YourDomain,DC=com
#   CN=John..Doe2,OU=Users,DC=YourDomain,DC=com
#   ..

from isc_transform_generator import *

# Define identity attributes
fn = identityAttribute("firstname")
ln = identityAttribute("lastname")

# Extract the first initial of the first name
fi = substring(begin=0, end=1, input=fn)

# Extract the first initial of the middle name
mi = substring(begin=0, end=1, input=identityAttribute("middlename"))

# Define patterns for the usernameGenerator transform
patterns = [
    "CN=$fi.$ln,OU=Users,DC=YourDomain,DC=com",
    "CN=$fn.$ln,OU=Users,DC=YourDomain,DC=com",
    "CN=$fn.$mi.$ln${uniqueCounter},OU=Users,DC=YourDomain,DC=com"
]

# Create the usernameGenerator transform
username_transform = usernameGenerator(
    patterns=patterns,
    source_check=True,
    cloud_max_size=100,
    cloud_max_unique_checks=5,
    fn=fn,
    ln=ln,
    fi=fi,
    mi=mi
)

# Generate the final transform output
transform(
    name="Create Unique distinguishedName",
    transform=username_transform
)


# RESULT:
'''
{
    "name": "Create Unique distinguishedName",
    "transform": {
        "type": "usernameGenerator",
        "attributes": {
            "sourceCheck": true,
            "patterns": [
                "CN=$fi.$ln,OU=Users,DC=YourDomain,DC=com",
                "CN=$fn.$ln,OU=Users,DC=YourDomain,DC=com",
                "CN=$fn.$mi.$ln${uniqueCounter},OU=Users,DC=YourDomain,DC=com"
            ],
            "fn": {
                "attributes": {
                    "name": "firstname"
                },
                "type": "identityAttribute"
            },
            "ln": {
                "attributes": {
                    "name": "lastname"
                },
                "type": "identityAttribute"
            },
            "fi": {
                "type": "substring",
                "attributes": {
                    "begin": 0,
                    "end": 1,
                    "input": {
                        "attributes": {
                            "name": "firstname"
                        },
                        "type": "identityAttribute"
                    }
                }
            },
            "mi": {
                "type": "substring",
                "attributes": {
                    "begin": 0,
                    "end": 1,
                    "input": {
                        "attributes": {
                            "name": "middlename"
                        },
                        "type": "identityAttribute"
                    }
                }
            }
        }
    },
    "attributes": {
        "cloudMaxSize": "100",
        "cloudMaxUniqueChecks": "5",
        "cloudRequired": "true"
    },
    "isRequired": false,
    "type": "string",
    "isMultiValued": false
}
'''
