from google_play_scraper import search, app

def main():

    results = search('idle game', n_hits=30)
    for result in results:
        print(result['appId'])
    # Get app information
    # app_info = app('com.king.candycrushsaga')
    # print(app_info)

if __name__ == '__main__':
    # Create a new instance of the ApkScraper class
    main()