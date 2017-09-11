#!/usr/bin/env python3
import sys
import json
import requests

from subprocess import call, check_output, run, Popen

def generate_static_reports(full_path, file_path):
    static_analysis_string = check_output(["peframe", "--json", file_path]).decode("utf-8")
    static_analysis_dict = json.loads(static_analysis_string)
    strings_report_string = check_output(["peframe", "--strings", file_path]).decode("utf-8")
    strings_report_dict = json.loads(strings_report_string)
    static_analysis_dict.update(strings_report_dict)
    final_string = json.dumps(static_analysis_dict, indent=4, sort_keys=False)
    with open(full_path + "/reports/static_analysis.json", "w+") as outputfile:
            outputfile.write(final_string)

def generate_dynamic_reports(full_path, file_path):
        Popen(["./src/queue_tools/push_line", "src/queue_tools/test", full_path, file_path])
        print("DYN REP WHRITTEN OK")
        

def generate_virus_total_reports(full_path, file_path):
        run(["./src/queue_tools/VTLockCheck", "src/queue_tools/virusTotalLock"])
        virus_total_string = json.dumps(virusTotal(file_path), indent=4, sort_keys=False)
        with open(full_path + "/reports/virus_total.json", "w+") as outputfile:
                outputfile.write(virus_total_string)

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

full_path = sys.argv[1]
file_path = sys.argv[2]
generate_dynamic_reports(full_path, file_path)
generate_static_reports(full_path, file_path)
generate_virus_total_reports(full_path, file_path)
print("SAVE FILE")
