import os
import subprocess
import csv
import pathlib

APK_FILE_PATH = "./apks"
DOCKER_FILE_PATH = "./apktool-docker"
IMAGE_NAME = "apktool-image"
CHECKED_APPS_CSV = "checked_app_id_list.csv"

def get_checked_apps():
    """Read the list of already checked apps from CSV."""
    checked_apps = set()
    if os.path.exists(CHECKED_APPS_CSV):
        try: 
            with open(CHECKED_APPS_CSV, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                checked_apps = {row[0] for row in reader}
        except:
            with open(CHECKED_APPS_CSV, 'w') as f:
                reader = csv.DictWriter(f)
                reader.writeheader(['id', 'isVulnerable'])
    return checked_apps

def build_docker():
    """Build the Docker image."""
    command = [
        "docker", "build",
        "-t", IMAGE_NAME,
        DOCKER_FILE_PATH
    ]
    subprocess.run(command, check=True)

def run_docker():
    """Run the Docker command to decompile APKs."""
    # Get list of already checked apps
    checked_apps = get_checked_apps()
    
    # Get list of APK files
    apk_files = [f for f in os.listdir(APK_FILE_PATH) if (f.endswith('.apk') or f.endswith('.xapk'))]
    
    for apk_file in apk_files:
        # Extract app ID from filename (removing .apk extension)
        app_id = pathlib.Path(apk_file).stem
        
        # Skip if already checked
        if app_id in checked_apps:
            print(f"Skipping {app_id} - already processed")
            continue
            
        command = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(APK_FILE_PATH)}:/apks",
            IMAGE_NAME,
            "d", f"/apks/{apk_file}",
            "-o", f"/apks/{apk_file}_decompiled"
        ]
        print(f"Decompiling {apk_file}...")
        subprocess.run(command, check=True)

def run_decompiler():
    build_docker()
    run_docker()

if __name__ == "__main__":
    run_decompiler()