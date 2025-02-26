import json

def flatten_text(input):
    if isinstance(input, str):
        return "".join(line.strip() for line in input.splitlines())
    else:
        return input

def transform(name, transform, requires_periodic_refresh=None):
    final_transform = {'name': name}
    final_transform.update(transform)
    if requires_periodic_refresh is not None:
        transform["attributes"]["requiresPeriodicRefresh"] = requires_periodic_refresh
    print(json.dumps(final_transform, indent=4))

def accountAttribute(source_name, attribute_name, account_sort_attribute=None, account_sort_descending=None, account_return_first_link=None, account_property_filter=None, account_filter=None):
    """
    Creates a dictionary representing an 'accountAttribute' transform in SailPoint.

    :param source_name: The name of the source where the account will be retrieved.
    :param attribute_name: The name of the attribute in the account to be returned.
    :param account_sort_attribute: (optional) Attribute used to sort accounts when selecting the value.
    :param account_sort_descending: (optional) Boolean indicating whether sorting should be in descending order.
    :param account_return_first_link: (optional) Boolean indicating whether to return the first account link found.
    :param account_property_filter: (optional) Filter to select accounts based on their properties.
    :param account_filter: (optional) Filter to select accounts based on specific criteria.
    :return: A dictionary representing the 'accountAttribute' transform.
    """
    transform = {
        "attributes": {
            "sourceName": source_name,
            "attributeName": attribute_name
        },
        "type": "accountAttribute"
    }
    if account_sort_attribute is not None:
        transform["attributes"]["accountSortAttribute"] = account_sort_attribute
    if account_sort_descending is not None:
        transform["attributes"]["accountSortDescending"] = account_sort_descending
    if account_return_first_link is not None:
        transform["attributes"]["accountReturnFirstLink"] = account_return_first_link
    if account_property_filter is not None:
        transform["attributes"]["accountPropertyFilter"] = account_property_filter
    if account_filter is not None:
        transform["attributes"]["accountFilter"] = account_filter
    return transform

def concat(values):
    """
    Creates a dictionary representing a 'concat' transform in SailPoint.

    :param values: List of values to be concatenated. Each value can be a static string or a dictionary representing another transformation.
    :return: A dictionary representing the 'concat' transform.
    """
    transform = {
        "attributes": {
            "values": values
        },
        "type": "concat"
    }
    return transform

def conditional(expression, positive_condition, negative_condition, requires_periodic_refresh=False, **variables):
    """
    Creates a dictionary representing a 'conditional' transform in SailPoint.

    :param expression: The conditional expression to evaluate, formatted as 'ValueA eq ValueB'.
    :param positive_condition: The output if the expression evaluates to true.
    :param negative_condition: The output if the expression evaluates to false.
    :param requires_periodic_refresh: Boolean indicating if the transform should be reevaluated during the nightly identity refresh process. Default is False.
    :param variables: Additional variables used in the expression, defined as keyword arguments.
    :return: A dictionary representing the 'conditional' transform.
    """
    attributes = {
        "expression": expression,
        "positiveCondition": positive_condition,
        "negativeCondition": negative_condition
    }
    attributes.update(variables)
    transform = {
        "attributes": attributes,
        "type": "conditional"
    }
    if requires_periodic_refresh:
        transform["requiresPeriodicRefresh"] = requires_periodic_refresh
    return transform


def dateCompare(first_date, second_date, operator, positive_condition="yes", negative_condition="no"):
    """
    Creates a dictionary representing a 'dateCompare' transform in SailPoint.

    :param first_date: First date for comparison (can be a string or a dictionary representing another transformation).
    :param second_date: Second date for comparison (can be a string or a dictionary representing another transformation).
    :param operator: Comparison operator ('LT', 'LTE', 'GT', 'GTE').
    :param positive_condition: Value returned if the comparison is true.
    :param negative_condition: Value returned if the comparison is false.
    :return: A dictionary representing the 'dateCompare' transform.
    """
    transform = {
        "attributes": {
            "firstDate": first_date,
            "secondDate": second_date,
            "operator": operator,
            "positiveCondition": positive_condition,
            "negativeCondition": negative_condition
        },
        "type": "dateCompare"
    }
    return transform

def dateFormat(input_format=None, output_format=None, input=None):
    """
    Creates a dictionary representing a 'dateFormat' transform in SailPoint.

    :param input_format: (optional) Input date format, either a string representing an explicit format or a predefined named format.
    :param output_format: (optional) Desired output date format, either a string representing an explicit format or a predefined named format.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'dateFormat' transform.
    """
    transform = {
        "attributes": {},
        "type": "dateFormat"
    }
    if input is not None:
        transform["attributes"]["input"] = input
    if input_format is not None:
        transform["attributes"]["inputFormat"] = input_format
    if output_format is not None:
        transform["attributes"]["outputFormat"] = output_format
    return transform

def dateMath(expression, round_up=None, input=None):
    """
    Creates a dictionary representing a 'dateMath' transform in SailPoint.

    :param expression: Expression that defines the date/time operations to be performed.
    :param round_up: (optional) Boolean indicating whether rounding should be up.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'dateMath' transform.
    """
    transform = {
        "attributes": {},
        "type": "dateMath"
    }
    if round_up is not None:
        transform["attributes"]["roundUp"] = round_up
    if input is not None:
        transform["attributes"]["input"] = input
    if expression is not None:
        transform["attributes"]["expression"] = expression
    return transform


def firstValid(values, ignore_errors=None):
    """
    Creates a dictionary representing a 'firstValid' transform in SailPoint.

    :param values: List of values to be evaluated. Each value can be a static string or a dictionary representing another transformation.
    :param ignore_errors: (optional) Boolean indicating whether to ignore errors and continue to the next value.
    :return: A dictionary representing the 'firstValid' transform.
    """
    transform = {
        "attributes": {
            "values": values
        },
        "type": "firstValid"
    }
    if ignore_errors is not None:
        transform["attributes"]["ignoreErrors"] = ignore_errors
    return transform

def getReferenceIdentityAttribute(uid, attribute_name):
    """
    Creates a dictionary representing a 'getReferenceIdentityAttribute' transform in SailPoint.

    :param uid: The unique identifier of the reference identity (e.g., "manager" or a specific user ID).
    :param attribute_name: The name of the attribute to retrieve from the reference identity.
    :return: A dictionary representing the 'getReferenceIdentityAttribute' transform.
    """
    transform = {
        "attributes": {
            "name": "Cloud Services Deployment Utility",
            "operation": "getReferenceIdentityAttribute",
            "uid": uid,
            "attributeName": attribute_name
        },
        "type": "rule"
    }
    return transform

def generateRandomString(length, include_numbers=True, include_special_chars=True):
    """
    Creates a dictionary representing a 'generateRandomString' transform in SailPoint.

    :param length: Length of the random string to be generated.
    :param include_numbers: (optional) Boolean indicating whether the string should include numbers.
    :param include_special_chars: (optional) Boolean indicating whether special characters should be included.
    :return: A dictionary representing the 'generateRandomString' transform.
    """
    transform = {
        "attributes": {
            "name": "Cloud Services Deployment Utility",
            "operation": "generateRandomString",
            "length": str(length),
            "includeNumbers": str(include_numbers).lower(),
            "includeSpecialChars": str(include_special_chars).lower()
        },
        "type": "rule"
    }
    return transform


def identityAttribute(attribute_name):
    """
    Creates a dictionary representing an 'identityAttribute' transform in SailPoint.

    :param attribute_name: The system (camel-cased) name of the identity attribute to retrieve.
    :return: A dictionary representing the 'identityAttribute' transform.
    """
    transform = {
        "attributes": {
            "name": attribute_name
        },
        "type": "identityAttribute"
    }
    return transform


def leftPad(length, padding=' ', input=None):
    """
    Creates a dictionary representing a 'leftPad' transform in SailPoint.

    :param length: Desired final length of the output string.
    :param padding: (optional) Character used for left-padding. Default is a space.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'leftPad' transform.
    """
    transform = {
        "type": "leftPad",
        "attributes": {
            "length": length,
            "padding": padding
        }
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def lookup(table, input=None):
    """
    Creates a dictionary representing a 'lookup' transform in SailPoint.

    :param table: Dictionary containing key-value pairs for matching.
                  Must include a 'default' key for unmatched values.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'lookup' transform.
    """
    if 'default' not in table:
        raise ValueError("The table must include a 'default' key for unmatched values.")

    transform = {
        "type": "lookup",
        "attributes": {
            "table": table
        }
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def lower(input=None):
    """
    Creates a dictionary representing a 'lower' transform in SailPoint.

    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'lower' transform.
    """
    transform = {
        "attributes": {},
        "type": "lower"
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def normalizeNames(input=None):
    """
    Creates a dictionary representing a 'nameNormalizer' transform in SailPoint.

    :param input_value: The input string to be normalized. If None, the transform will use the default input from the source attribute.
    :return: A dictionary representing the 'nameNormalizer' transform.
    """
    transform = {
        "type": "normalizeNames"
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def rightPad(length, padding=' ', input=None):
    """
    Creates a dictionary representing a 'rightPad' transform in SailPoint.

    :param length: Desired final length of the output string.
    :param padding: (optional) Character used for right-padding. Default is a space.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'rightPad' transform.
    """
    transform = {
        "type": "rightPad",
        "attributes": {
            "length": length,
            "padding": padding
        }
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def randomAlphaNumeric(length=32):
    """
    Creates a dictionary representing a 'randomAlphaNumeric' transform in SailPoint.

    :param length: (optional) Desired length of the generated string. Default is 32.
    :return: A dictionary representing the 'randomAlphaNumeric' transform.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")
    if length > 450:
        raise ValueError("Maximum allowed length is 450 characters.")

    transform = {
        "attributes": {
            "length": length
        },
        "type": "randomAlphaNumeric"
    }
    return transform


def randomNumeric(length=32):
    """
    Creates a dictionary representing a 'randomNumeric' transform in SailPoint.

    :param length: (optional) Desired length of the generated string. Default is 32.
    :return: A dictionary representing the 'randomNumeric' transform.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")
    if length > 450:
        raise ValueError("Maximum allowed length is 450 characters.")

    transform = {
        "attributes": {
            "length": length
        },
        "type": "randomNumeric"
    }
    return transform


def reference(transform_id, input=None):
    """
    Creates a dictionary representing a 'reference' transform in SailPoint.

    :param transform_id: ID of the transform being referenced.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'reference' transform.
    """
    transform = {
        "attributes": {
            "id": transform_id
        },
        "type": "reference"
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def replace(regex, replacement, input=None):
    """
    Creates a dictionary representing a 'replace' transform in SailPoint.

    :param regex: Regular expression pattern to be replaced.
    :param replacement: Replacement string for the matched pattern.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'replace' transform.
    """
    transform = {
        "attributes": {
            "regex": regex,
            "replacement": replacement
        },
        "type": "replace"
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def replaceAll(table, input=None):
    """
    Creates a dictionary representing a 'replaceAll' transform in SailPoint.

    :param table: Dictionary containing regex patterns and their respective replacement values.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'replaceAll' transform.
    """
    if not isinstance(table, dict) or not table:
        raise ValueError("The table must be a non-empty dictionary containing regex-replacement pairs.")

    transform = {
        "attributes": {
            "table": table
        },
        "type": "replaceAll"
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def substring(begin, end=None, begin_offset=None, end_offset=None, input=None):
    """
    Creates a dictionary representing a 'substring' transform in SailPoint.

    :param begin: Starting index (zero-based) for the substring.
    :param end: (optional) Ending index (zero-based) where the substring ends.
                If not provided or set to -1, it will include the string until the end.
    :param begin_offset: (optional) Number of characters to add to the 'begin' index.
    :param end_offset: (optional) Number of characters to add to the 'end' index.
    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'substring' transform.
    """
    transform = {
        "type": "substring",
        "attributes": {
            "begin": begin
        }
    }
    if end is not None:
        transform["attributes"]["end"] = end
    if begin_offset is not None:
        transform["attributes"]["beginOffset"] = begin_offset
    if end_offset is not None:
        transform["attributes"]["endOffset"] = end_offset
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def split(delimiter, index, input=None, throws=True):
    """
    Creates a dictionary representing a 'split' transform in SailPoint.

    :param delimiter: Character or regex used to split the input string.
    :param index: Index of the desired element after splitting (zero-based).
    :param input: (optional) Dictionary defining the input for the transform.
    :param throws: (optional) Boolean indicating whether an exception should be raised
                   if the index is out of bounds.
    :return: A dictionary representing the 'split' transform.
    """
    transform = {
        "type": "split",
        "attributes": {
            "delimiter": delimiter,
            "index": index
        }
    }
    if input is not None:
        transform["attributes"]["input"] = input
    if throws is not None:
        transform["attributes"]["throws"] = throws
    return transform


def static(value, variables=None):
    """
    Creates a dictionary representing a 'static' transform in SailPoint.

    :param value: The fixed value or VTL expression to be returned by the transform.
    :param variables: An optional dictionary of variables to be used in the VTL expression.
    :return: A dictionary representing the 'static' transform.
    """
    transform = {
        "attributes": {},
        "type": "static"
    }
    if variables:
        transform["attributes"].update(variables)
    if value:
        transform["attributes"]['value'] = flatten_text(value)
    return transform


def trim(input=None):
    """
    Creates a dictionary representing a 'trim' transform in SailPoint.

    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'trim' transform.
    """
    transform = {
        "type": "trim"
    }
    attributes = {}
    if input is not None:
        attributes["input"] = input
    if attributes:
        transform["attributes"] = attributes
    return transform


def upper(input=None):
    """
    Creates a dictionary representing an 'upper' transform in SailPoint.

    :param input: (optional) Dictionary defining the input for the transform.
    :return: A dictionary representing the 'upper' transform.
    """
    transform = {
        "type": "upper",
        "attributes": {}
    }
    if input is not None:
        transform["attributes"]["input"] = input
    return transform


def usernameGenerator(patterns, source_check=True, cloud_max_size=255, cloud_max_unique_checks=50, **variables):
    """
    Creates a dictionary representing a 'usernameGenerator' transform in SailPoint.

    :param patterns: A list of patterns to generate the username. Example: ["$fi.$ln", "$fn.$ln", "$fi$ln"]
    :param source_check: Boolean indicating whether to check for uniqueness in the source. Default is True.
    :param cloud_max_size: Maximum length of the generated username. Default is 255.
    :param cloud_max_unique_checks: Maximum number of uniqueness checks to attempt. Default is 50.
    :param variables: Additional variables used in patterns, defined as keyword arguments.
                      Example: fi=first initial, ln=last name, fn=first name.
    :return: A dictionary representing the 'usernameGenerator' transform.
    """
    # Construct the attributes dictionary
    attributes = {
        "sourceCheck": source_check,
        "patterns": patterns
    }
    
    # Add provided variables to the attributes
    for var_name, transform in variables.items():
        attributes[var_name] = transform

    # Construct the complete transform dictionary
    transform = {
        "type": "usernameGenerator",
        "attributes": attributes
    }
    cloud_attributes = {
        "cloudMaxSize": str(cloud_max_size),
        "cloudMaxUniqueChecks": str(cloud_max_unique_checks),
        "cloudRequired": "true"
    }
    
    return {"transform": transform, "attributes": cloud_attributes, "isRequired": False, "type": "string", "isMultiValued": False}

