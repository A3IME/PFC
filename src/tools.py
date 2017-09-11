import requests
import sys
import json

def virusTotal(path):
    params = {'apikey': '95237e1de590ecf93b71c02679cd6ba797497f8d4aa3bd5483f2b51bb4015708'}
    files = {'file': (path, open(path, 'rb'))}
    response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
    json_response = response.json()


    params['resource'] = str(json_response['resource'])

    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent" : "gzip, My python requests library example client or username",
    }

    new_response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
    resp = new_response.json()
    #print(resp)
    return resp

