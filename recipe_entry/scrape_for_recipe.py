from recipe_scrapers import scrape_me
from time import sleep

file_name = input("File that contains all of the URLs to recipes")
with open(file_name) as f:
    for line in f:
        url = line.rstrip('\n')
        try:
            scraper = scrape_me(url)
            print(scraper.ingredients())
        except:
            sleep(5)
            continue