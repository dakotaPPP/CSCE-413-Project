import argparse
import os
import csv
from scraper import run_scraper
from decompile import run_decompiler

APP_ID_LIST = "app_id_list.csv"
CHECKED_APP_ID_LIST = "checked_app_id_list.csv"

# Command line arguments
parser = argparse.ArgumentParser(description="APK Scraper")
parser.add_argument("-s", "--search", type=str, required=True, help="Search term for fetching app IDs")
parser.add_argument("-n", "--number-of-apks", type=int, required=True, help="Number of APKs to download")
args = parser.parse_args()

SEARCH_TERM_FOR_APP_IDS = args.search
NUMBER_OF_APKS_TO_DOWNLOAD = args.number_of_apks

if not os.path.exists("apks"):
    os.makedirs("apks")

def update_checked_list():
    """Move downloaded app IDs from app_id_list.csv to checked_app_id_list.csv."""
    if not os.path.exists(APP_ID_LIST):
        return
    
    # Read new app IDs
    new_checked_ids = set()
    with open(APP_ID_LIST, mode="r", newline="") as file:
        new_checked_ids.update(row[0] for row in csv.reader(file))
    
    # Load existing checked IDs and their vulnerability status
    existing_data = {}
    if os.path.exists(CHECKED_APP_ID_LIST):
        with open(CHECKED_APP_ID_LIST, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            existing_data = {row['id']: row['isVulnerable'] for row in reader}
    
    # Merge existing and new data
    for app_id in new_checked_ids:
        if app_id not in existing_data:
            existing_data[app_id] = "false"
    
    # Write updated data back to checked_app_id_list.csv
    with open(CHECKED_APP_ID_LIST, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "isVulnerable"])  # Write header
        for app_id, is_vulnerable in existing_data.items():
            writer.writerow([app_id, is_vulnerable])
    
    os.remove(APP_ID_LIST)  # Cleanup after processing



def main():
    run_scraper(SEARCH_TERM_FOR_APP_IDS, NUMBER_OF_APKS_TO_DOWNLOAD)
    run_decompiler()
    update_checked_list()

if __name__ == "__main__":
    main()
