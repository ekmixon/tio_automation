#!/usr/bin/env python3
#Disclaimer: This is NOT supported By Tenable!

# This script pauses all Nessus Scans

import requests

# avoid insecure warning
requests.packages.urllib3.disable_warnings()


#avoid insecure warning
requests.packages.urllib3.disable_warnings()

def grab_headers():
    #Enter Your Access keys
    access_key = ''
    secret_key = ''

    return {
        'Content-type': 'application/json',
        'X-ApiKeys': f'accessKey={access_key};secretKey={secret_key}',
    }


def get_data(url_mod):
    #Base URL
    url = "https://cloud.tenable.com"
    #Retreive Headers
    headers = grab_headers()
    #API Call
    r = requests.request('GET', url + url_mod, headers=headers, verify=False)
    #return data in json format
    return r.json()

def post_data(url_mod):
    #Base URL
    url = "https://cloud.tenable.com"
    #Retreive Headers
    headers = grab_headers()
    #return raw response
    return requests.post(url + url_mod, headers=headers, verify=False)

def main():
    # grab all of the scans in t.io
    data = get_data('/scans')

    # loop through each scan
    for scans in data['scans']:

        # idenify those that are running to be paused
        if scans['status'] == "paused" and scans['type'] == "remote":
                # try block to ignore errors
            try:
                # need the ID for alerting the user
                id = scans['id']

                    # request the scan be paused
                post = post_data(f'/scans/{str(id)}/resume')

                    # decide what to do based on HTTP Codes
                if post.status_code == 200:
                    print(f" Your Scan {str(id)} Resumed")
                elif post.status_code == 409:
                    print("Wait a few seconds and try again")
                elif post.status_code == 404:
                    print("yeah, this scan doesn't exist")
                else:
                    print("It's possible this is already running")

            except:
                pass


if __name__ == '__main__':
    main()
