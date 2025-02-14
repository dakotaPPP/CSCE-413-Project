from google_play_scraper import search
import csv
import subprocess
import os

# File paths
APP_ID_LIST = "app_id_list.csv"
CHECKED_APP_ID_LIST = "checked_app_id_list.csv"
OUTPUT_PATH = "./apks" 

# TODO - turn these into command line arguments
SEARCH_TERM_FOR_APP_IDS = "idle game" 
NUMBER_OF_APKS_TO_DOWNLOAD = 10

def fetch_app_ids():
    searchResults = search(SEARCH_TERM_FOR_APP_IDS, n_hits=NUMBER_OF_APKS_TO_DOWNLOAD)
    return [result['appId'] for result in searchResults]


def load_checked_ids():
    """Load already downloaded app IDs from checked_app_id_list.csv."""
    if not os.path.exists(CHECKED_APP_ID_LIST):
        return set()
    
    with open(CHECKED_APP_ID_LIST, mode="r", newline="") as file:
        return {row[0] for row in csv.reader(file)}

def save_app_ids(filename, app_ids):
    """Save app IDs to a CSV file."""
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        for app_id in app_ids:
            writer.writerow([app_id])

def run_docker():
    """Run the Docker command to download APKs."""
    command = [
        "docker", "run", "--rm",
        "-v", f"{os.path.abspath(OUTPUT_PATH)}:/output",
        "-v", f"{os.path.abspath(APP_ID_LIST)}:/app_id_list.csv",
        "ghcr.io/efforg/apkeep:stable",
        "-c", "/app_id_list.csv", "/output"
    ]
    subprocess.run(command, check=True)

def update_checked_list():
    """Move downloaded app IDs from app_id_list.csv to checked_app_id_list.csv."""
    if not os.path.exists(APP_ID_LIST):
        return
    
    new_checked_ids = set()
    with open(APP_ID_LIST, mode="r", newline="") as file:
        new_checked_ids.update(row[0] for row in csv.reader(file))
    
    checked_ids = load_checked_ids()
    checked_ids.update(new_checked_ids)

    save_app_ids(CHECKED_APP_ID_LIST, checked_ids)
    os.remove(APP_ID_LIST)  # Cleanup after processing

def main():
    app_ids = fetch_app_ids()
    checked_ids = load_checked_ids()
    
    new_app_ids = [app_id for app_id in app_ids if app_id not in checked_ids]
    
    if not new_app_ids:
        print("No new APKs to download.")
        return
    
    save_app_ids(APP_ID_LIST, new_app_ids)
    
    try:
        run_docker()
        update_checked_list()
        print("APK download process completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during APK download: {e}")

if __name__ == "__main__":
    main()
