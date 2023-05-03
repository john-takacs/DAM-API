from typing import Dict

import requests
import authorization_v2

"""
Description:
AMR API Retrieval Script
This Python script provides functions for retrieving AMR information from the MX

Author: John Takacs
Email: john.takacs@me.com
Creation date: 2023-05-02
Developer note: This is code from my personal lab for my professional development. This should be considered example 
code only.

Revision History:
-----------------
2023-05-02:
    Initial creation of the script.    
"""

# Global variables
HOST = "3.231.102.188"
#HOST = "44.192.43.91"
PORT = "8083"
BASIC_AUTHORIZATION = 'Basic YWRtaW46SWhhdGQyZUV0TWhj'
DEBUG = False


def get_agent_monitoring_rule(rule_name, headers):
    """
    Retrieves an agent monitoring rule by its name.

    Args:
        rule_name (str): The name of the agent monitoring rule.

    Returns:
        dict: The agent monitoring rule information as a dictionary,
              or None if the rule is not found.
    """
    url = f"https://{HOST}:{PORT}/SecureSphere/api/v1/conf/agentsMonitoringRules/{rule_name}"

    print(url)
    #
    # headers = {
    #     "Content-Type": "application/json",
    #     "Cookie": "JSESSIONID=0123456789ABCDEF0123456789ABCDEF"
    # }
    #body = {'policy-type':'ds-agents-monitoring-rules'}
    body = {}

    response = requests.post(url, json=body, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"Successfully retrieved : {rule_name}")
    else:
        print("Error Code:  " + str(response.status_code))
        print(
            f"Failed to retrieve AMR: {rule_name}\nHere is the error message: {response.text}")


if __name__ == '__main__':
    # Get the session_id via get_cookie()
    my_response = authorization_v2.authorization()
    my_cookies = authorization_v2.get_cookie(my_response, DEBUG)
    headers: Dict[str, str] = {"Content-Type": "application/json", "Authorization": BASIC_AUTHORIZATION,
                               'Cookie': my_cookies}
    if my_response.status_code == 200:
        # The request was successful
        print("\nThe initial login request was successful\nWe will now retrieve the AMR")
        rule_name = "create_table_dictionary"
        rule = get_agent_monitoring_rule(rule_name, headers)
        if rule is not None:
            print("Agent Monitoring Rule:")
            print(rule)
        else:
            print(f"Agent Monitoring Rule '{rule_name}' not found.")

    else:
        # The request was not successful
        print(f'Request failed with status code {my_response.status_code}')