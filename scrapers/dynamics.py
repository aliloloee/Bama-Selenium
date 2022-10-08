try :
    from scrapers.base_driver import DynamicDriverSetUp
except :
    from base_driver import DynamicDriverSetUp
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import time


class BamaScraper(DynamicDriverSetUp) :

    def _create_url(self, category, endpoint='') :
        if not (category in self.allowed_categories) :
            raise ValueError('Category not allowed')
        url = self.base_url+category.lower()

        if endpoint.strip() == '' :
            return url
        elif endpoint[0] not in ['?', '/'] :
            endpoint = '/' + endpoint
        return url + endpoint

    def _analyse_add_or_pin(self, ad) :
        try :
            r = ad.find("div", class_="bama-ad__time").find('span').get_text()
        except :
            r = ad.find("div", class_="bama-ad__pin-badge").find('span').get_text()
        return r

    def _check_and_scroll(self, url, target) :
        self.driver.get(url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True :
            elements = self.driver.find_elements(By.CSS_SELECTOR, '.bama-ad-container .bama-ad')
            if len(elements) > target :
                break

            #* Scrolling down, up and down again for the new items to show up 
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            self.driver.execute_script("scrollBy(0,-500);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height :
                break
            last_height = new_height

    def scrape(self, category, endpoint=None, target=10) :
        url = self._create_url(category, endpoint)
        self._check_and_scroll(url, target)

        response = BS(self.driver.page_source, "html.parser")
        self._end_driver()

        items = []
        for item in response.select('.bama-ad-container .bama-ad') :
            items.append({
                'name' : item.find("div", class_="bama-ad__title").get_text(),
                'add_time' : self._analyse_add_or_pin(item),
                'price' : item.find("div", class_="bama-ad__price-holder").find("span").get_text(),
                'address' : item.find("div", class_="bama-ad__address-holder").find("span").get_text(),
                'url' : self.base_url+item['href'][1:]
            })

        return {category: items}


if __name__ == '__main__' :
    bbs = BamaScraper()
    category = 'car'
    endpoint = 'amico'
    target = 20
    items = bbs.scrape(category, endpoint, target)
    print(items)