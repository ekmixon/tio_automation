#!/usr/bin/env python3
#Disclaimer: This is NOT supported By Tenable!

#The code below is basic code to retreive data from tio using the requests library
import requests
import pprint

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

def main():
    #grab all of the scans in t.io
    data = get_data('/scans')

    #print out a formated version of the response
    pprint.pprint(data)


if __name__ == '__main__':
    main()