import os
import subprocess
import csv
import pathlib
import zipfile
import shutil

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
                f.write("id,isVulnerable\n")
    return checked_apps

def build_docker():
    """Build the Docker image."""
    command = [
        "docker", "build",
        "-t", IMAGE_NAME,
        DOCKER_FILE_PATH
    ]
    subprocess.run(command, check=True)

def extract_xapk(xapk_path, output_dir):
    """Extract APKs from XAPK file."""
    with zipfile.ZipFile(xapk_path, 'r') as xapk:
        xapk.extractall(output_dir)
    # Find all APKs in the extracted directory
    extracted_apks = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.apk'):
                extracted_apks.append(os.path.join(root, file))
    return extracted_apks

def run_docker():
    """Run the Docker command to decompile APKs."""
    checked_apps = get_checked_apps()
    files = [f for f in os.listdir(APK_FILE_PATH) if (f.endswith('.apk') or f.endswith('.xapk'))]
    
    for file in files:
        file_path = os.path.join(APK_FILE_PATH, file)
        app_id = pathlib.Path(file).stem
        
        if app_id in checked_apps:
            print(f"Skipping {app_id} - already processed")
            continue
            
        if file.endswith('.xapk'):
            print(f"Processing XAPK: {file}")
            # Create temporary directory for extraction
            temp_dir = os.path.join(APK_FILE_PATH, f"{app_id}_temp")
            # Create main decompiled directory for this XAPK
            main_output_dir = os.path.join(APK_FILE_PATH, f"{app_id}_decompiled")
            
            os.makedirs(temp_dir, exist_ok=True)
            os.makedirs(main_output_dir, exist_ok=True)
            os.chmod(temp_dir, 0o777)
            os.chmod(main_output_dir, 0o777)
            
            try:
                # Extract all APKs from XAPK
                extracted_apks = extract_xapk(file_path, temp_dir)
                
                # Decompile each extracted APK
                for idx, apk in enumerate(extracted_apks):
                    apk_filename = os.path.basename(apk)
                    apk_name = os.path.splitext(apk_filename)[0]
                    # Put the decompiled APK in a subdirectory of the main XAPK directory
                    output_dir = f"{app_id}_decompiled/{apk_name}"
                    
                    command = [
                        "docker", "run", "--rm",
                        "-v", f"{os.path.abspath(APK_FILE_PATH)}:/apks",
                        "--user", f"{os.getuid()}:{os.getgid()}",
                        IMAGE_NAME,
                        "d", f"/apks/{app_id}_temp/{apk_filename}",
                        "-o", f"/apks/{output_dir}"
                    ]
                    print(f"Decompiling {apk_filename} from XAPK...")
                    subprocess.run(command, check=True)
                    
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
                
        else:  # Regular APK file
            command = [
                "docker", "run", "--rm",
                "-v", f"{os.path.abspath(APK_FILE_PATH)}:/apks",
                IMAGE_NAME,
                "d", f"/apks/{file}",
                "-o", f"/apks/{app_id}_decompiled"
            ]
            print(f"Decompiling {file}...")
            subprocess.run(command, check=True)

def run_decompiler():
    build_docker()
    run_docker()

if __name__ == "__main__":
    run_decompiler()