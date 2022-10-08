from scrapers.statics import BamaBrandScraper, BamaCityScraper, BamaDetailsScraper


# * highlight=True --> opens the browser and highlights every element that is being scraped
# * there are some time.sleep() codes in highlighting elements, thats why highlight=True 
# * takes too much time to scrape the whole part
# * Set hightlight to False to skip GUI and the time.sleep() lines to scrape quickly


# bbs = BamaDetailsScraper(highlight=True)
# bbs = BamaCityScraper(highlight=True)
bbs = BamaBrandScraper(highlight=True)
path = bbs.scrape(category='car')  # category='motorcycle'
print(path)

