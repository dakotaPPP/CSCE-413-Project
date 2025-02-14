# APK Scraper

This project is a Python script that automates the process of downloading APK files from the Google Play Store based on a search term. The script uses Docker to run the APK downloader.

## Prerequisites

- Python 3.x
- Docker

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd apk-scraper
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure Docker is installed and running on your system. You can download Docker from [here](https://www.docker.com/products/docker-desktop).

## Usage

1. Open the `main.py` file and modify the following variables as needed:
    - `SEARCH_TERM_FOR_APP_IDS`: The search term to find apps on the Google Play Store.
    - `NUMBER_OF_APKS_TO_DOWNLOAD`: The number of APKs to download based on the search term.

2. Run the script:
    ```sh
    python main.py
    ```

## What the Script Does

1. **Fetch App IDs**: The script searches the Google Play Store for apps matching the specified search term and retrieves their app IDs.
2. **Load Checked IDs**: It loads the list of already downloaded app IDs from `checked_app_id_list.csv`.
3. **Save New App IDs**: It saves the new app IDs to `app_id_list.csv`.
4. **Run Docker**: The script runs a Docker container to download the APKs using the app IDs in `app_id_list.csv`.
5. **Update Checked List**: After downloading, it moves the downloaded app IDs from `app_id_list.csv` to `checked_app_id_list.csv` and deletes `app_id_list.csv`.

## Directory Structure

- `apks/`: Directory where the downloaded APK files are saved.
- `app_id_list.csv`: Temporary file that stores the app IDs to be downloaded.
- `checked_app_id_list.csv`: File that stores the app IDs that have already been downloaded.
- `main.py`: The main script that performs the APK downloading process.

## Notes

- Ensure Docker is properly installed and running before executing the script.
- The script will only download APKs that have not been previously downloaded, as tracked by `checked_app_id_list.csv`.

## License

This project is licensed under the MIT License.