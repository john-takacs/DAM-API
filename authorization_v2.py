import requests
import urllib3
from requests import Response

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Description:
This Python script provides functions for logging in to the MX using Basic Authorization and retrieving the session cookies.

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

# Global variables
HOST = "3.231.102.188"
PORT = "8083"
BASIC_AUTHORIZATION = 'Basic YWR'
DEBUG = True

def authorization(debug=False):
    """
    This function logs in to the MX using Basic Authorization.

    A Basic Authentication Header Generator can be found here: https://mixedanalytics.com/tools/basic-authentication-generator/

    The user must be an MX Admin GUI user.  admin:somePassword is the syntax.

    Only two variables need to be modified prior to use:
    1. url
    2. headers (Encoded credentials to base 64)

    :param debug:
    :type debug: Boolean necessary to enable/disable
    :return: Returns the requests.Response
    :rtype: <class 'requests.models.Response'>
    """
    url = f"https://{HOST}:{PORT}/SecureSphere/api/v1/auth/session"
    payload = {}
    headers = dict(Authorization=BASIC_AUTHORIZATION)
    auth_response: Response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    if debug:
        print(f"Request URL: {auth_response.request.url}")
        print(f"Request Headers: {auth_response.request.headers}")
        print(f"Request Body: {auth_response.request.body}")
        print(f"Response Status Code: {auth_response.status_code}")
        print(f"Response Headers: {auth_response.headers}")
        print(f"Response Cookies: {auth_response.cookies}")
        print(f"Response Body (response.text): {auth_response.text}")
        print(f"Successfully logged in with session ID: {auth_response.request.url}")
        print(f"response.cookies and response.text both have the session-id's")
    else:
        # print(f"Failed to log in: {auth_response.text}")
        pass

    return auth_response


def get_cookie(response, debug):
    """
    This function extracts the session cookies from the response.

    :param response: (Response) The response from the authorization request.
    :param debug: (bool) Whether to enable debug mode or not.
    :return: (str) Returns the cookies in string format.
    """
    sso_id = response.cookies.get('SSOSESSIONID')
    j_id = response.cookies.get('JSESSIONID')
    # cookie = f"'Cookie': 'JSESSIONID={j_id}; SSOSESSIONID={sso_id}'"
    # cookie = f"'JSESSIONID={j_id}; SSOSESSIONID={sso_id}'"
    cookie = f"JSESSIONID={j_id}; SSOSESSIONID={sso_id}"
    if debug == True:
        print(cookie)
    return cookie


if __name__ == '__main__':
    debug = DEBUG
    response: object = authorization(debug)

    if response.status_code == 200:
        # The authorization request was successful
        print("\nThe authorization request was successful")
        content = response.text
        if debug == True:
            print(f"Response cookies: {response.cookies}")
            print(f"Response Body: {response.text}")
            print("Sending to get_cookie()")
        get_cookie(response, debug)


    else:
        # The request was not successful
        print(f'Request failed with status code {response.status_code}')
