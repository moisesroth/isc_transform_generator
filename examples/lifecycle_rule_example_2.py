# Lifecycle Rule Transform that classifies users into the statuses:
#   - active
#   - inactive
#   - inactiveImmediate
#   - prehire
#   - prehireover30days
#   - post30days
#   - notmapped (fallback)

from isc_transform_generator import *

# Collecting hire date and formatting it
hire_date = dateFormat(
    input_format="MM/dd/yyyy",
    output_format="ISO8601",
    input=firstValid([
        accountAttribute("Workday", "HIREDATE"),
        static("12/31/1900")  # Default value to prevent nulls
    ])
)

# Collecting termination date and formatting it
termination_date = dateFormat(
    input_format="MM/dd/yyyy",
    output_format="ISO8601",
    input=firstValid([
        accountAttribute("Workday", "TERMINATION_DATE"),
        static("12/31/2500")  # Default value to prevent nulls
    ])
)

# Checks if the hire date is in the future
hiring_in_future = dateCompare(
    first_date=hire_date,
    second_date="now",
    operator="gt",
    positive_condition="yes",
    negative_condition="no"
)

# Checks if hire date is within the next 30 days
hiring_within_30_days = dateCompare(
    first_date=hire_date,
    second_date=dateMath(expression="now+30d/d", round_up=False),
    operator="lt",
    positive_condition="yes",
    negative_condition="no"
)

# Checks if termination date is in the past or today
terminated = dateCompare(
    first_date=termination_date,
    second_date="now",
    operator="lte",
    positive_condition="yes",
    negative_condition="no"
)

# Checks if termination was more than 30 days ago
terminated_over_30_days = dateCompare(
    first_date=termination_date,
    second_date=dateMath(expression="now-30d/d", round_up=False),
    operator="lt",
    positive_condition="yes",
    negative_condition="no"
)

# Immediate termination flag from source
terminated_immediately = lookup(
    table={
        "1": "yes",
        "true": "yes",
        "yes": "yes",
        "Yes": "yes",
        "default": "no"
    },
    input=accountAttribute("Workday", "Immediate_Termination__c")
)

# Termination flag from source
terminated_flag = lookup(
    table={
        "1": "yes",
        "default": "no"
    },
    input=accountAttribute("Workday", "TERMINATED")
)

# Final classification rule using Velocity
velocity_script = '''
#if( $terminated_over_30_days == 'yes' )
    post30days
#elseif( $terminated_immediately == 'yes' )
    inactiveImmediate
#elseif( $terminated == 'yes' && $terminated_flag == 'yes' )
    inactive
#elseif( $hiring_in_future == 'yes' && $hiring_within_30_days == 'yes' )
    prehire
#elseif( $hiring_in_future == 'yes' )
    prehireover30days
#elseif( $terminated == 'no' )
    active
#else
    notmapped
#end
'''

# Defining Lifecycle Status transform
transform_value = static(
    value=velocity_script,
    variables={
        "hiring_in_future": hiring_in_future,
        "hiring_within_30_days": hiring_within_30_days,
        "terminated": terminated,
        "terminated_over_30_days": terminated_over_30_days,
        "terminated_immediately": terminated_immediately,
        "terminated_flag": terminated_flag
    }
)

transform("Lifecycle State Transform", transform_value, requires_periodic_refresh=True)

# RESULT:
'''
{
    "name": "Lifecycle State Transform",
    "attributes": {
        "hiring_in_future": {
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
                                            "value": "12/31/1900"
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
                "operator": "gt",
                "positiveCondition": "yes",
                "negativeCondition": "no"
            },
            "type": "dateCompare"
        },
        "hiring_within_30_days": {
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
                                            "value": "12/31/1900"
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
                        "roundUp": false,
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
        "terminated": {
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
        "terminated_over_30_days": {
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
                        "roundUp": false,
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
        "terminated_immediately": {
            "type": "lookup",
            "attributes": {
                "table": {
                    "1": "yes",
                    "true": "yes",
                    "yes": "yes",
                    "Yes": "yes",
                    "default": "no"
                },
                "input": {
                    "attributes": {
                        "sourceName": "Workday",
                        "attributeName": "Immediate_Termination__c"
                    },
                    "type": "accountAttribute"
                }
            }
        },
        "terminated_flag": {
            "type": "lookup",
            "attributes": {
                "table": {
                    "1": "yes",
                    "default": "no"
                },
                "input": {
                    "attributes": {
                        "sourceName": "Workday",
                        "attributeName": "TERMINATED"
                    },
                    "type": "accountAttribute"
                }
            }
        },
        "value": "#if( $terminated_over_30_days == 'yes' )post30days#{elseif}( $terminated_immediately == 'yes' )inactiveImmediate#{elseif}( $terminated == 'yes' && $terminated_flag == 'yes' )inactive#{elseif}( $hiring_in_future == 'yes' && $hiring_within_30_days == 'yes' )prehire#{elseif}( $hiring_in_future == 'yes' )prehireover30days#{elseif}( $terminated == 'no' )active#{else}notmapped#end",
        "requiresPeriodicRefresh": true
    },
    "type": "static"
}
'''
