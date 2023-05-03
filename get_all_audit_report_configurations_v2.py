import requests
import authorization_v2
from typing import Dict, List

"""
This script retrieves all flattened DB Audit report configurations and returns them as a JSON list.
Author: John Takacs
Email: john.takacs@imperva.com
Creation Date: April 6th, 2023
Developer note: This is code from my personal lab environment. This should be considered example 
code only, to be used as a guide in further customization for your environment. 

Revision History:
-----------------
2023-02-23:
    Initial creation of the script.  
"""

# Global variables
HOST = "192.168.102.188"
PORT = "8083"
BASIC_AUTHORIZATION = 'Basic YWR'
DEBUG = True


def get_all_audit_report_configurations(headers: Dict[str, str]) -> List[Dict]:
    """
    Retrieve all flattened DB Audit report configurations.

    Details:
    The function takes a single parameter named headers which is of type Dict[str, str]. This means that headers is a
    dictionary that has string keys and string values. The headers dictionary is used to specify the authorization and
    content-type headers in the GET request.
    :param headers: Headers for authorization and content-type
    :return: JSON list containing all flattened DB Audit report configurations
    """
    # Desired URL for sonar migration
    url = f"https://{HOST}:{PORT}/SecureSphere/api/v1/conf/jsonar/dbauditreports/"
    # Test URL
    #url = f"https://{HOST}:{PORT}/SecureSphere/api/v1/conf/dbauditreports/"
    if DEBUG:
        print(f"This is the url: {url}")
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


if __name__ == '__main__':
    """
        Entry point of the script. This code will execute only if this script is run directly, not if it is imported as 
        a module. It retrieves all flattened DB Audit report configurations using the 
        `get_all_audit_report_configurations` function and prints them to the console.
        """
    # Get the session_id via get_cookie()
    my_response = authorization_v2.authorization()
    my_cookies = authorization_v2.get_cookie(my_response, DEBUG)
    headers: Dict[str, str] = {"Content-Type": "application/json", "Authorization": BASIC_AUTHORIZATION,
                               'Cookie': my_cookies}
    if my_response.status_code != 200:
        # The request was not successful
        print(f'Request failed with status code {my_response.status_code}')

    else:
        # The request was successful
        all_configs = get_all_audit_report_configurations(headers)
        print(all_configs)
