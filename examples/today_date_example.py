# This transform sets the AD "description" attribute with a predefined text followed by today's date.
#   - The text "Created by ISC " is used as a prefix.
#   - The current date is dynamically appended in the format YYYY-MM-DD.
#   - The result is a string like: "Created by ISC 2025-03-04".


from isc_transform_generator import *

# Get today's date in the format YYYY-MM-DD
today_date = dateFormat(
    input=dateMath(expression="now"),
    input_format="yyyy-MM-dd",
    output_format="yyyy-MM-dd"
)

# Concatenate "Created by ISC" with today's date
description_value = concat(
    values=[
        static("Created by ISC "),
        today_date
    ]
)

# Generate the transform
transform("Set Description with Today Date", description_value)


# RESULT:
'''
{
    "name": "Set Description with Today Date",
    "attributes": {
        "values": [
            {
                "attributes": {
                    "value": "Created by ISC "
                },
                "type": "static"
            },
            {
                "attributes": {
                    "input": {
                        "attributes": {
                            "expression": "now"
                        },
                        "type": "dateMath"
                    },
                    "inputFormat": "yyyy-MM-dd",
                    "outputFormat": "yyyy-MM-dd"
                },
                "type": "dateFormat"
            }
        ]
    },
    "type": "concat"
}
'''
