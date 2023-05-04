import json
from typing import Dict

import pandas as pd
import requests
import authorization_v2

"""
This script reads data from an input CSV file, converts it to a JSON string, and iterates through each row of the data 
to create a protected IP list on a specified server group in Imperva SecureSphere using the API.
 
It utilizes two functions: create_protected_ip_list and read_csv.

Usage:
1. Modify the CSV file to reflect your desired entries.
2. Edit the name of the input CSV file: input_csv_filename = "input.csv"
3. Modify the headers (Encoded credentials to base 64)
4. Execute

Author: John Takacs
Email: john.takacs@me.com
Creation Date: 2023-02-23
Developer note: This is code from my personal lab for my professional development. This should be considered example 
code only.

Revision History:
-----------------
2023-02-23:
    Initial creation of the script.  
"""

# Important filename variable
input_csv_filename = "input.csv"

def create_protected_ip_list(host, port, site_name, server_group_name, ip_address, gateway_group_name, body, headers):
    """
    Creates a protected IP list on a specified server group in Imperva SecureSphere using the API.

    :param host: The hostname or IP address of the Imperva SecureSphere Management Server
    :param port: The port number of the Imperva SecureSphere Management Server
    :param site_name: The name of the site in Imperva SecureSphere
    :param server_group_name: The name of the server group in Imperva SecureSphere
    :param ip_address: The IP address to be added to the protected IP list
    :param gateway_group_name: The name of the gateway group in Imperva SecureSphere
    :param body: The JSON body of the POST request
    :param headers: The headers of the POST request

    :return: None
    """
    url: str = f"https://{host}:{port}/SecureSphere/api/v1/conf/serverGroups/{site_name}/{server_group_name}/protectedIPs/{ip_address}?gatewayGroup={gateway_group_name}"
    response = requests.post(url, json=body, headers=headers, verify=False)
    if response.status_code == 200:
        # The Server Group IP's are created by default
        print(f"Successfully created Protected and Server Group IP address: {ip_address}")
    else:
        print("Error Code:  " + str(response.status_code))
        print(
            f"Failed to create Protected and Server Group IP address : {ip_address}\nHere is the error message: {response.text}")


def read_csv(debug):
    """
    Reads data from an input CSV file, converts it to a JSON string, and returns it as a dictionary.

    :param debug: A boolean flag indicating whether to enable debugging

    :return: A dictionary containing the data from the input CSV file
    """
    # Read CSV file
    data = pd.read_csv(input_csv_filename)

    # Convert DataFrame to JSON string
    json_string = data.to_json(orient='records')
    # Convert data to dictionary
    data = json.loads(json_string)
    if debug == True:
        print(type(data))
        print(data)
        # Print JSON string
        print("This is json_string")
        print(json_string)
        print("This is data")
        print(type(data))
        print("This is data[0]")
        print(data[0])
        print(type(data[0]))
    return data


if __name__ == '__main__':
    """Create protected IP lists for SecureSphere using data from a CSV file.

    This script reads data from a CSV file and uses it to create protected IP lists in SecureSphere.
    It first logs in to SecureSphere using the `authorization` module and gets an authorization cookie,
    then uses this cookie to make API requests to create the protected IP lists.

    Usage:
    $ python create_protected_ip_list_v2.py
    """
    debug = False
    data = read_csv(debug)
    # Get the session_id via get_cookie()
    my_response = authorization.authorization()
    my_cookies = authorization.get_cookie(my_response, debug)
    headers: Dict[str, str] = {"Content-Type": "application/json", "Authorization": "Basic Y=",
                               'Cookie': my_cookies}
    if my_response.status_code == 200:
        # The request was successful
        print("\nThe initial login request was successful\nWe will now begin creating the Protected IP's and the Server"
              " Group IP's")
        # Iterate through the dictionary
        assert isinstance(data, object)
        count = len(data)
        rownum: int = 1
        for row in data:
            print(f"\nInserting row {str(rownum)}:  Site: {row['site']} and IP: {row['ip-address']}")
            original_dict = row
            mx_host: str = row['MX-IP']
            mx_port: str = row['MX-port']
            site_name: str = row['site']
            server_group_name: str = row['server_group_name']
            service_name: str = row['service_name']
            connection_name: str = row['connection_name']
            ip_address: str = row['ip-address']
            gateway_group_name: str = row['gateway_group_name']
            comment = row['comment']
            assert isinstance(comment, object)
            # body = {'comment': '16-Jan-23'}
            body = {'comment': comment}
            create_protected_ip_list(mx_host, mx_port, site_name, server_group_name, ip_address, gateway_group_name, body,
                                     headers)
            rownum: int = rownum + 1
    else:
        # The request was not successful
        print(f'Request failed with status code {my_response.status_code}')
