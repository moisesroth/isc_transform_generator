# Here is the Lifecycle Rule Transform that classifies users into the statuses:
#   - Active
#   - Inactive
#   - Terminated
#   - Pre-hired
#   - Terminated + 30 days

from isc_transform_generator import *

# Collecting hire date
hire_date = dateFormat(
    input_format="MM/dd/yyyy",
    output_format="ISO8601",
    input=firstValid([
        accountAttribute("Workday", "HIREDATE"),
        static("12/31/2500")  # Default value to prevent nulls
    ])
)

# Collecting termination date
termination_date = dateFormat(
    input_format="MM/dd/yyyy",
    output_format="ISO8601",
    input=firstValid([
        accountAttribute("Workday", "TERMINATION_DATE"),
        static("12/31/2500")  # Default value to prevent nulls
    ])
)

# Pre-hire (30 days before start date)
pre_hired = dateCompare(
    first_date=hire_date,
    second_date=dateMath(expression="now+30d/d"),
    operator="lt",
    positive_condition="yes",
    negative_condition="no"
)

# Active (hire date <= today)
active = dateCompare(
    first_date=hire_date,
    second_date="now",
    operator="lte",
    positive_condition="yes",
    negative_condition="no"
)

# Inactive (termination date <= today)
inactive = dateCompare(
    first_date=termination_date,
    second_date="now",
    operator="lte",
    positive_condition="yes",
    negative_condition="no"
)

# Terminated + 30 days (termination date < today - 30 days)
terminated_30 = dateCompare(
    first_date=termination_date,
    second_date=dateMath(expression="now-30d/d"),
    operator="lt",
    positive_condition="yes",
    negative_condition="no"
)

# Immediate termination flag
immediate_flag = lookup(
    table={
        "true": "yes",
        "yes": "yes",
        "default": "no"
    },
    input=accountAttribute("Workday", "Inactive")
)

# Velocity Rule
velocity_rule = '''
#if( $pre_hired == 'yes' )
    Pre-Hired
#elseif( $inactive == 'yes' )
    #if( $terminated_30 == 'yes' )
        Terminated + 30 Days
    #else
        Terminated
    #end
#elseif( $active == 'yes' )
    Active
#else
    Inactive
#end
'''

# Defining Lifecycle Status transform
lifecycle_status = static(
    value=velocity_rule,
    variables={
        "pre_hired": pre_hired,
        "active": active,
        "inactive": inactive,
        "terminated_30": terminated_30,
        "immediate_flag": immediate_flag
    }
)

# Generate the transform
transform("Lifecycle Status Rule", lifecycle_status)

# RESULT:
'''
{
    "name": "Lifecycle Status Rule",
    "attributes": {
        "pre_hired": {
            "attributes": {
                "firstDate": {
                    "attributes": {
                        "input": {
                            "attributes": {
                                "values": [
                                    {
                                        "attributes": {
                                            "sourceName": "Workday",
                                            "attributeName": "HIREDATE"
                                        },
                                        "type": "accountAttribute"
                                    },
                                    {
                                        "attributes": {
                                            "value": "12/31/2500"
                                        },
                                        "type": "static"
                                    }
                                ]
                            },
                            "type": "firstValid"
                        },
                        "inputFormat": "MM/dd/yyyy",
                        "outputFormat": "ISO8601"
                    },
                    "type": "dateFormat"
                },
                "secondDate": {
                    "attributes": {
                        "expression": "now+30d/d"
                    },
                    "type": "dateMath"
                },
                "operator": "lt",
                "positiveCondition": "yes",
                "negativeCondition": "no"
            },
            "type": "dateCompare"
        },
        "active": {
            "attributes": {
                "firstDate": {
                    "attributes": {
                        "input": {
                            "attributes": {
                                "values": [
                                    {
                                        "attributes": {
                                            "sourceName": "Workday",
                                            "attributeName": "HIREDATE"
                                        },
                                        "type": "accountAttribute"
                                    },
                                    {
                                        "attributes": {
                                            "value": "12/31/2500"
                                        },
                                        "type": "static"
                                    }
                                ]
                            },
                            "type": "firstValid"
                        },
                        "inputFormat": "MM/dd/yyyy",
                        "outputFormat": "ISO8601"
                    },
                    "type": "dateFormat"
                },
                "secondDate": "now",
                "operator": "lte",
                "positiveCondition": "yes",
                "negativeCondition": "no"
            },
            "type": "dateCompare"
        },
        "inactive": {
            "attributes": {
                "firstDate": {
                    "attributes": {
                        "input": {
                            "attributes": {
                                "values": [
                                    {
                                        "attributes": {
                                            "sourceName": "Workday",
                                            "attributeName": "TERMINATION_DATE"
                                        },
                                        "type": "accountAttribute"
                                    },
                                    {
                                        "attributes": {
                                            "value": "12/31/2500"
                                        },
                                        "type": "static"
                                    }
                                ]
                            },
                            "type": "firstValid"
                        },
                        "inputFormat": "MM/dd/yyyy",
                        "outputFormat": "ISO8601"
                    },
                    "type": "dateFormat"
                },
                "secondDate": "now",
                "operator": "lte",
                "positiveCondition": "yes",
                "negativeCondition": "no"
            },
            "type": "dateCompare"
        },
        "terminated_30": {
            "attributes": {
                "firstDate": {
                    "attributes": {
                        "input": {
                            "attributes": {
                                "values": [
                                    {
                                        "attributes": {
                                            "sourceName": "Workday",
                                            "attributeName": "TERMINATION_DATE"
                                        },
                                        "type": "accountAttribute"
                                    },
                                    {
                                        "attributes": {
                                            "value": "12/31/2500"
                                        },
                                        "type": "static"
                                    }
                                ]
                            },
                            "type": "firstValid"
                        },
                        "inputFormat": "MM/dd/yyyy",
                        "outputFormat": "ISO8601"
                    },
                    "type": "dateFormat"
                },
                "secondDate": {
                    "attributes": {
                        "expression": "now-30d/d"
                    },
                    "type": "dateMath"
                },
                "operator": "lt",
                "positiveCondition": "yes",
                "negativeCondition": "no"
            },
            "type": "dateCompare"
        },
        "immediate_flag": {
            "type": "lookup",
            "attributes": {
                "table": {
                    "true": "yes",
                    "yes": "yes",
                    "default": "no"
                },
                "input": {
                    "attributes": {
                        "sourceName": "Workday",
                        "attributeName": "Inactive"
                    },
                    "type": "accountAttribute"
                }
            }
        },
        "value": "#if( $pre_hired == 'yes' )Pre-Hired#{elseif}( $inactive == 'yes' )#if( $terminated_30 == 'yes' )Terminated + 30 Days#{else}Terminated#end#{elseif}( $active == 'yes' )Active#{else}Inactive#end"
    },
    "type": "static"
}
'''
