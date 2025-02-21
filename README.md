# ISC Transform Generator  

## Overview  
**ISC Transform Generator** is a Python-based utility designed to streamline the creation of **SailPoint Identity Security Cloud (ISC) transforms**. This tool automates the generation of valid JSON configurations, reducing manual effort and ensuring consistency in IAM workflows.  

## Features  
- ✅ **Predefined Transform Functions** – Includes common ISC transforms like `accountAttribute`, `concat`, `dateCompare`, `lookup`, `static`, `replace`, and more.
- ✅ **Automated JSON Generation** – Eliminates manual JSON creation and formatting errors.
- ✅ **Easily Expandable** – Supports adding new transforms as needed.


## Examples  

Here are some examples demonstrating how to use **ISC Transform Generator** to create different ISC transforms.  

### **📌 Checking If a User Was Terminated More Than 30 Days Ago**  
This transform checks if the `TERMINATION_DATE` is older than `today - 30 days`.  

#### **Use Case**  
This is useful for identifying users who have been terminated for more than 30 days, allowing automated deprovisioning of accounts and access cleanup.  

#### **Python Code**  
```python
from transform_tools_v3 import *

transform("Terminated Over 30 Days Ago",
    dateCompare(
        first_date=dateFormat(
            input_format="MM/dd/yyyy",
            output_format="ISO8601",
            input=firstValid([
                accountAttribute("Workday", "TERMINATION_DATE"),
                static("12/31/2500")  # Default fallback to avoid null values
            ])
        ),
        second_date=dateMath(
            expression="now-30d/d",
            round_up=False
        ),
        operator="lt",
        positive_condition="yes",
        negative_condition="no"
    )
)
```

### **📌 Retrieving the Best Available Email for a User**  
This transform retrieves the best available email address for a user, prioritizing Active Directory (AD). If no email is found in AD, it will check Workday. If neither source provides an email, a default value indicating the absence of an email will be used.  

#### **Use Case**  
This is useful for ensuring that every user has a valid email address for communication and account provisioning. By following a priority order, this transform guarantees that the best possible email is assigned while also providing a fallback value when no email is found.  

#### **Python Code**  
```python
from transform_tools_v3 import *

transform("Best Available Email",
    firstValid([
        accountAttribute("AD", "mail"),
        accountAttribute("Workday", "mail"),
        static("no-email@example.com")  # Default fallback if no email is found
    ])
)
```



