from scrapers.dynamics import BamaScraper


category = 'car'
endpoint = '?brand=amico&brand=alfaromeo,giulietta'    # an endpoint or query or ...
target = 20      # number of items you want to scrape (the number of scraped items goes beyond this but never less)
bs = BamaScraper()
items = bs.scrape(category, endpoint, target)
print(items[category])

