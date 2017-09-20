#!/usr/bin/env python3
from distutils.dir_util import copy_tree
from shutil import copyfile
import sys
import os
import json
import requests
import time
import shutil
from json2html import *

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

    with open(full_path + "/reports/static_analysis.html", "w+") as outputfile:
        outputfile.write(json2html.convert(json = static_analysis_dict))

def generate_dynamic_reports(full_path, file_path):
	REST_URL = "http://localhost:8090/tasks/create/file"
	FILE = file_path
	
	with open(FILE, "rb") as sample:
		files = {"file": ("temp_file_name", sample)}
		r = requests.post(REST_URL,  files=files)

	task_id = r.json()["task_id"]
	
	status = 'not reported'
	#print(status)
	
	while status != 'reported':
		r = requests.get("http://localhost:8090/tasks/view/" + str(task_id))
		status = r.json()["task"]["status"]
		#print(status)
		time.sleep(60)
	os.chdir(full_path + "/reports")
	path_analyses_cuckoo = "/home/artefathos/.cuckoo/storage/analyses/" + str(task_id)
	shutil.make_archive("Arquivos_Analise_Dinamica", "zip", path_analyses_cuckoo)
	
	copyfile(path_analyses_cuckoo + "/reports/report.html", full_path + "/dynamic_analysis.html") 
	#print("DYN REP WHRITTEN OK")
        

def generate_virus_total_reports(full_path, file_path):
        run(["./src/queue_tools/VTLockCheck", "src/queue_tools/virusTotalLock"])
        virus_total_string = json.dumps(virusTotal(file_path), indent=4, sort_keys=False)
        with open(full_path + "/reports/virus_total.json", "w+") as outputfile:
                outputfile.write(virus_total_string)

        virus_total_dict = json.loads(virus_total_string)
        with open(full_path + "/reports/virus_total.html", "w+") as outputfile:
            outputfile.write(json2html.convert(json = virus_total_dict))

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
generate_static_reports(full_path, file_path)
generate_virus_total_reports(full_path, file_path)
generate_dynamic_reports(full_path, file_path)
#print("SAVE FILE")
