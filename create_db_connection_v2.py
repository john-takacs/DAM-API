from typing import Dict, Any

import requests
import authorization_v2
import pandas as pd
import json

"""
This script is used to create multiple database connections (aliases) via API calls. The input data is stored in a CSV
file named input.csv. This file must include several columns of data that will be used to create the connection. The
script will read in the data from the CSV file, create a dictionary, and iterate over each row of the dictionary to
make the appropriate API calls to create the connection. If an API call is successful, a message will be printed to the
console indicating the connection was created. If the call fails, an error message will be printed to the console.

It utilizes two functions: create_db_connection and read_csv.

Usage:
1. Modify the CSV file to reflect your desired entries.
2. Edit the name of the input CSV file: input_csv_filename = "input.csv"
3. Modify the headers (Encoded credentials to base 64)
4. Execute

Author: John Takacs
Email: john.takacs@me.com
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

def create_db_connection(host, port, site_name, server_group_name, service_name, connection_name, body, headers):
    """
    Makes an API call to create a database connection (alias).

    :param host: A string representing the host name
    :param port: A string representing the port number
    :param site_name: A string representing the site name
    :param server_group_name: A string representing the server group name
    :param service_name: A string representing the service name
    :param connection_name: A string representing the connection name
    :param body: A dictionary representing the data to send to the API
    :param headers: A dictionary representing the headers to send with the API request

    :return: None
    """
    url: str = f"https://{host}:{port}/SecureSphere/api/v1/conf/dbServices/{site_name}/{server_group_name}/{service_name}/dbConnections/{connection_name}"
    response = requests.post(url, json=body, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"Successfully created database connection with alias: {connection_name}")
    else:
        print("Error Code:  " + str(response.status_code))
        print(
            f"Failed to create database connection with alias: {connection_name}\nHere is the error message: {response.text}")

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
    """Create db connections (aliases) for SecureSphere using data from a CSV file.

    This script reads data from a CSV file and uses it to create db connections (aliases) in SecureSphere.
    It first logs in to SecureSphere using the `authorization` module and gets an authorization cookie,
    then uses this cookie to make API requests to create the db connections.
        
    Usage:
    $ python create_db_connection_v2.py
    """
    debug = True
    data = read_csv(debug)
    # Get the session_id via get_cookie()
    my_response = authorization.authorization()
    my_cookies = authorization.get_cookie(my_response, debug)
    headers: Dict[str, str] = {"Content-Type": "application/json", "Authorization": "Basic MjM=",
                               'Cookie': my_cookies}
    if my_response.status_code == 200:
        # The request was successful
        print("\nThe initial login request was successful\nWe will now begin creating a db connection (alias) for each"
              " of the Protected IP's")
        # Iterate through the dictionary
        assert isinstance(data, object)
        count = len(data)
        rownum = 1
        for row in data:
            print(f"\nInserting row {str(rownum)}:  {row['connection_name']}")
            original_dict = row
            # Each row is everything in the CSV file.  Not all API calls will require every parameter. This next step
            # creates a smaller dictionary from the original row of data.
            keys = ('MX-IP', 'MX-port', 'site', 'server_group_name', 'service_name', 'connection_name', 'ip-address',
                    'OS-type', 'user-name', 'password','named-instance','domain-name', 'port')
            new_dict: Dict[str, Any] = dict((k, original_dict[k]) for k in keys if k in original_dict)
            if debug:
                print(f"This is the row {row}")
                print(f"This is the new_dict {new_dict}")
            body = new_dict
            # Parameters for the MX and Site Tree hierarchy.
            # Troubleshooting
            mx_host: str = body['MX-IP']
            #host: str = ""
            mx_port: str = body['MX-port']
            #port: str = "8083"
            site_name: str = body['site']
            server_group_name: str = body['server_group_name']
            service_name: str = body['service_name']
            connection_name: str = body['connection_name']
            # Send parameters to create_db_connection()
            create_db_connection(mx_host, mx_port, site_name, server_group_name, service_name, connection_name, body, headers)
            rownum = rownum + 1
    else:
        # The request was not successful
        print(f'Request failed with status code {my_response.status_code}')
