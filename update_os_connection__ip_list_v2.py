from typing import Dict
import requests
import authorization_v2
import pandas as pd
import json

"""
This script updates the OS of the list of IP's in the Server's tab.

Usage:
1. Modify the input.csv  file to reflect your desired entries.
2. If you change the name of the input file, then edit this variable:  input_csv_filename = "input.csv"
3. Modify the headers (Encoded credentials to base 64)
4. Execute

Author: John Takacs
Email: john.takacs@gmail.com
Creation date: 2023-02-23
Developer note: This is code from my personal lab for my professional development. This should be considered example 
code only.

Revision History:
-----------------
2023-02-23:
    Initial creation of the script.    

"""

# Important filename variable
input_csv_filename = "input.csv"


def update_server_group_iplist(host: str, port: str, site_name: str, server_group_name: str, ip_address: str,
                               body: Dict[str, str], headers: Dict[str, str]) -> None:
    """
    Updates the OS of a server group IP address.

    Args:
    - host (str): the server host name or IP address
    - port (str): the server port number
    - site_name (str): the name of the site
    - server_group_name (str): the name of the server group
    - ip_address (str): the IP address of the server to update
    - body (Dict[str, str]): the request body containing the updated OS type
    - headers (Dict[str, str]): the request headers

    Returns: None
    """
    # https://docs.imperva.com/bundle/v14.7-dam-api-reference-guide/page/61821.htm
    # URL must match https://{host:port}/SecureSphere/api/v1/conf/serverGroups/{siteName}/{serverGroupName}/servers/{ip}
    url: str = f"https://{host}:{port}/SecureSphere/api/v1/conf/serverGroups/{site_name}/{server_group_name}/servers/{ip_address}"

    response = requests.put(url, json=body, headers=headers, verify=False)

    if response.status_code == 200:
        print(f"Successfully updated OS for IP address: {ip_address}")
    else:
        print("Error Code:  " + str(response.status_code))
        print(f"Failed to update OS for IP address : {ip_address}\nHere is the error message: {response.text}")


def read_csv(debug: bool) -> Dict:
    """
    Reads a CSV file and returns a dictionary containing the file data.
    Args:
    - debug (bool): if True, print additional debug information

    Returns:
    - data (Dict): a dictionary containing the file data
    """
    # Read CSV file
    data = pd.read_csv(input_csv_filename)

    # Convert DataFrame to JSON string
    json_string = data.to_json(orient='records')
    # Convert data to dictionary
    data = json.loads(json_string)
    if debug:
        print(type(data))
        assert isinstance(data, object)
        print(data)
        # Print JSON string
        print("This is json_string")
        print(json_string)
        print("This is data")
        print(type(data))
        print("This is data[0]")
        print(data[0])
        print(type(data[0]))
    # body=data[0]
    # comment = {"comment": "Some comment"}
    # body = comment
    return data


'''
This script reads data from a CSV file and uses it to update the OS of the protected IP lists in SecureSphere.
It first logs in to SecureSphere using the `authorization` module and gets an authorization cookie, 
then uses this cookie to make API requests to update the OS.

Steps
Updates the OS of the list of IP's in the Server's tab by:
1. Iterating through a dictionary of server data; and
2. Calling the 'update_server_group_iplist' function for each server

The 'debug' flag controls whether additional debug information is printed.

Args: None
Returns: None
Raises: None

Usage:
$ python update_os_connection_ip_list_v2.py
'''
if __name__ == '__main__':
    debug = False
    data = read_csv(debug)
    # Get the session_id via get_cookie()
    my_response = authorization.authorization()
    my_cookies = authorization.get_cookie(my_response, debug)
    headers: Dict[str, str] = {"Content-Type": "application/json", "Authorization": "Basic YtW4",
                               'Cookie': my_cookies}
    if my_response.status_code == 200:
        # The request was successful
        print("\nThe initial login request was successful\nWe will now begin updating the OS Server Group"
              " IP's")
        # Iterate through the dictionary
        assert isinstance(data, object)
        count = len(data)
        print(count)
        rownum = 1
        for row in data:
            print(f"\nUpdating row {str(rownum)}:  {row['ip-address']}")
            if debug:
                print(f"This is the row {row}")
            host: str = row['MX-IP']
            port: str = row['MX-port']
            site_name: str = row['site']
            server_group_name: str = row['server_group_name']
            service_name: str = row['service_name']
            connection_name: str = row['connection_name']
            ip_address: str = row['ip-address']
            gateway_group_name: str = row['gateway_group_name']
            os_type = row['OS-type']
            assert isinstance(os_type, object)
            body = {'OS-type': os_type}
            print(body)
            update_server_group_iplist(host, port, site_name, server_group_name, ip_address, body, headers)
            rownum = rownum + 1

    else:
        # The request was not successful
        print(f'Request failed with status code {my_response.status_code}')
