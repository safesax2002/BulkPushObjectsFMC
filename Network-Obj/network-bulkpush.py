"""
This python module was created by Shubham Bharti.
Feel free to send comments/suggestions/improvements.  Either by email: shbharti@cisco.com or more importantly via a pull
request from the github repository: https://github.com/shubhambharti89/FMCAPI
"""

import requests
import json
import time
from requests.auth import HTTPBasicAuth
from getpass import getpass
import customfunctions as cf

addr = input("Enter IP Address of the FMC: ")
username = input ("Enter Username: ")
password = getpass("Enter Password: ")

csvFilePath = input("Please enter the CSV Filepath (For eg. : path/to/file/objects.csv) :")

api_uri = "/api/fmc_platform/v1/auth/generatetoken"

url = "https://" + addr + api_uri
response = requests.post(url, verify=False, auth=HTTPBasicAuth(username, password))

accesstoken = response.headers["X-auth-access-token"]
refreshtoken = response.headers["X-auth-refresh-token"]
DOMAIN_UUID = response.headers["DOMAIN_UUID"]


host,ranges,network,fqdn = cf.csvtojson(csvFilePath)

host_payload = json.dumps(host)
range_payload = json.dumps(ranges)
network_payload = json.dumps(network)
fqdn_payload = json.dumps(fqdn)

host_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/hosts?bulk=true"
range_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/ranges?bulk=true"
network_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/networks?bulk=true"
fqdn_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/fqdns?bulk=true"


host_url = "https://" + addr + host_api_uri
network_url = "https://" + addr + network_api_uri
range_url = "https://" + addr + range_api_uri
fqdn_url = "https://" + addr + fqdn_api_uri

headers = {
  'Content-Type': 'application/json',
  'x-auth-access-token': accesstoken
}

logfile = "log_"+ str(time.perf_counter_ns()) + ".txt"

if host != []:
    response = requests.request("POST", host_url, headers=headers, data = host_payload, verify = False)

    if response.status_code == 201 or response.status_code == 202:
        print("Host Objects successfully pushed")

    else:
        print("Host Object creation failed")


    log = open(logfile,"w+")
    log.write(response.text)
    log.close

if ranges != []:
    response = requests.request("POST", range_url, headers=headers, data = range_payload, verify = False)

    if response.status_code == 201 or response.status_code == 202:
        print("Range Objects successfully pushed")

    else:
        print("Range Object creation failed")


    log = open(logfile,"a+")
    log.write(response.text)
    log.close

if network != []:
    response = requests.request("POST", network_url, headers=headers, data = network_payload, verify = False)

    if response.status_code == 201 or response.status_code == 202:
        print("Network Objects successfully pushed")

    else:
        print("Network Object creation failed")


    log = open(logfile,"a+")
    log.write(response.text)
    log.close
    
if fqdn != []:
    response = requests.request("POST", fqdn_url, headers=headers, data = fqdn_payload, verify = False)

    if response.status_code == 201 or response.status_code == 202:
        print("FQDN Objects successfully pushed")

    else:
        print("FQDN Object creation failed")


    log = open(logfile,"a+")
    log.write(response.text)
    log.close

else :
    print("Please Validate that the CSV file provided is correct or at correct location")
