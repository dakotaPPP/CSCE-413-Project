import os
import requests
import json
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder

SERVER_URL = "http://localhost:8000"
API_KEY = "api key from mobsf docker"

APKS_FOLDER = "./apks"
RESULTS = "./results"

# Finish this part of organizing and making a leaderboard
VERY_HIGH_RISK_DIR = os.path.join(RESULTS, "very_high_risk")
HIGH_RISK_DIR = os.path.join(RESULTS, "high_risk")
MEDIUM_RISK_DIR = os.path.join(RESULTS, "medium_risk")
LOW_RISK_DIR = os.path.join(RESULTS, "low_risk")

def sort_scorecard(report_json):
    security_score = report_json.get("security_score")
    if security_score < 30:
        return VERY_HIGH_RISK_DIR
    elif security_score < 40:
        return HIGH_RISK_DIR
    elif security_score < 60:
        return MEDIUM_RISK_DIR
    else:
        return LOW_RISK_DIR

def upload(file):
    print("uploading APK")
    data = MultipartEncoder(fields={'file': (file, open(file, 'rb'), 'application/octet-stream')})
    headers = {'Content-Type': data.content_type, 'Authorization': API_KEY}
    response = requests.post(SERVER_URL + '/api/v1/upload', data=data, headers=headers)
    print(response.text)
    if response.status_code == 200:
        return response.json() 
    else:
        print(f"Error uploading APK: {response.text}")
        return None

def scan(apk_hash):
    print("scanning APK : ", apk_hash)

    scan_data = {
        "hash": apk_hash,
        "re_scan": 0
    }

    headers = {'Authorization': API_KEY}
    response = requests.post(SERVER_URL + '/api/v1/scan', data=scan_data, headers=headers)

    # print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error scanning APK: {response.text}")
        return None


def report(apk_hash):
    print("generating Report on APK")
    headers = {'Authorization': API_KEY}
    response = requests.post(SERVER_URL + '/api/v1/scorecard', data={"hash": apk_hash}, headers=headers)
    # print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching report: {response.text}")
        return None

scan_results = {}

for file in os.listdir(APKS_FOLDER):
    if(file.endswith(".apk") or file.endswith(".xapk")): 
        apk_path = os.path.join(APKS_FOLDER, file)

        safe_filename = file.replace(".", "_")
        # scorecard_file = os.path.join(RESULTS, f"{safe_filename}_scorecard.json")

        upload_response = upload(apk_path)
        if upload_response and "hash" in upload_response:
            apk_hash = upload_response["hash"]
            scan_response = scan(apk_hash)
            if scan_response:
                report_data = report(apk_hash)
                if report_data:
                    # with open(scorecard_file, 'w') as f:
                    #     json.dump(report_data, f, indent=2)
                    # print(f"Scorecard saved to: {scorecard_file}")

                    catagorized_dir = sort_scorecard(report_data)
                    sorted_file_path = os.path.join(catagorized_dir, f"{safe_filename}_scorecard.json")
                    with open(sorted_file_path, 'w') as f:
                        json.dump(report_data, f, indent=2)
                    print(f"scorecard saved to: {sorted_file_path}\n")
                     
print("[+] Scan completed [+]")