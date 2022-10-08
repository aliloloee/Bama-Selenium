try :
    from scrapers.base_driver import DriverSetUp
except :
    from base_driver import DriverSetUp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import time, os, json


class BamaBrandScraper(DriverSetUp) :
    def __init__(self, highlight, *args, **kwargs) :
        super().__init__(highlight, *args, **kwargs)
        self.prefix = 'brand'

    def _create_url(self, category) :
        if not (category in self.allowed_categories) :
            raise ValueError('Category not allowed')
        return f'{self.base_url}{category.lower()}'

    def _check_item_existance(self, parsed_text) :
        if parsed_text.find("i", class_="bama-icon-checkbox-outlined-bold") :
            return True
        return False

    def _get_brand_links(self, progress_bar=False) :
        items = {}
        p = len(self.driver.find_elements(By.CSS_SELECTOR, ".stepped-selection__list div"))

        if progress_bar :
            print(f'Scraping {self.prefix} --> {self.cat} section')
            valid_range = self._progressBar(range(1,p+1), prefix = 'Progress:', suffix = 'Complete', length=50)
        else :
            valid_range = range(1, p+1)

        for i in valid_range :
            elm = self.driver.find_element(By.XPATH, f"(//div[contains(@class, 'stepped-selection__list-item')])[{i}]")
            self._highlight(elm)

            parsed_text = BS(elm.get_attribute('innerHTML'), "html.parser")
            text = parsed_text.find("span", class_="stepped-selection__list-item-title").get_text().strip()

            if self._check_item_existance(parsed_text) :
                endpoint = elm.get_attribute('data-trackervalue').replace(',','-')
                # items.append({text:endpoint})
                items[text] = endpoint
                continue

            self.driver.execute_script("arguments[0].click();", elm)
            sub_items = self._get_brand_links()
            # items.append({text:sub_items})
            items[text] = sub_items

        try :
            back_btn = self.driver.find_element(By.XPATH, "//div[@class='stepped-selection__header-navigation']")
            self._highlight(back_btn)
            self.driver.execute_script("arguments[0].click();", back_btn)
        except :
            close_btn = self.driver.find_element(By.XPATH, "//button[@class='stepped-selection__close-button']")
            self._highlight(close_btn)
            self.driver.execute_script("arguments[0].click();", close_btn)
        
        return items

    def scrape(self, category) :
        self.cat = category
        self.driver.get(self._create_url(category))
        try:
            brand = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '(//div[@class="bama-filter__container"])[1]/div/div/div/div'))
            )
        except Exception as e :
            # print(e)
            self.driver.quit()

        self.driver.execute_script("arguments[0].click();", brand)
        self.driver.implicitly_wait(5)

        all_brands = self._get_brand_links(progress_bar=True)
        file_path = f"schemas/{self.prefix}/{category}.json"
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_brands, f, ensure_ascii=False, indent=4)
        return file_path


class BamaCityScraper(BamaBrandScraper) :
    def __init__(self, highlight, *args, **kwargs) :
        super().__init__(highlight, *args, **kwargs)
        self.prefix = 'city'

    def scrape(self, category) :
        self.cat = category
        self.driver.get(self._create_url(category))
        try:
            city = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '((//div[@class="bama-filter__container"])[2]/div/div/div/div)[1]'))
            )
        except Exception as e :
            # print(e)
            self.driver.quit()

        self.driver.execute_script("arguments[0].click();", city)
        self.driver.implicitly_wait(5)

        all_cities = self._get_brand_links(progress_bar=True)
        file_path = f"schemas/{self.prefix}/{category}.json"
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_cities, f, ensure_ascii=False, indent=4)
        return file_path


class BamaDetailsScraper(BamaBrandScraper) :
    def __init__(self, highlight, *args, **kwargs) :
        super().__init__(highlight, *args, **kwargs)
        self.prefix = 'detail'
        # self.ex_word = 'desktop'
        self.exceptional_detail = 'رنگ بدنه'

    def _highlight(self, element):
        if self.highlight :
            super()._highlight(element)
        else :
            time.sleep(1)

    def _get_query_keyword(self, base_addr) :
        checkbox = self.driver.find_element(By.XPATH, f'{base_addr}/div/label')
        self._highlight(checkbox)
        checkbox.click()
        time.sleep(2)
        query_keyword = self.driver.current_url.split('?')[1].split('=')[0]
        self.driver.back()
        time.sleep(2)
        return query_keyword

    def _get_brand_links(self, progress_bar=False) :
        items = {}
        p = len(self.driver.find_elements(By.XPATH, "//div[@class='bama-checkbox-accordion']"))

        if progress_bar :
            print(f'Scraping {self.prefix} --> {self.cat} section')
            print('This might take a while, be patient ...')
            valid_range = self._progressBar(range(1,p+1), prefix = 'Progress:', suffix = 'Complete', length=50)
        else :
            valid_range = range(1, p+1)

        for i in valid_range :
            elm = self.driver.find_element(By.XPATH, f"(//div[@class='bama-checkbox-accordion__toggler'])[{i}]")

            self._highlight(elm)
            parsed_text = BS(elm.get_attribute('innerHTML'), "html.parser")
            text = parsed_text.find("span", class_="bama-checkbox-accordion__toggler-text").get_text().strip()

            # self.driver.execute_script("arguments[0].click();", elm)
            elm.click()
            self.driver.implicitly_wait(10)


            try :
                load_more = elm.find_element(By.XPATH, f"(//div[@class='bama-checkbox-accordion__checkbox-container'])[{i}]/div[@class='bama-checkbox-accordion__load-more']/span")
            except :
                load_more = None

            if load_more :
                self._highlight(load_more)
                load_more.click()
                self.driver.implicitly_wait(5)

            p2 = len(self.driver.find_elements(By.XPATH, "//div[@class='bama-checkbox-accordion__checkbox-container']/div/div/div[@class='bama-checkbox']"))

            sub_details = []
            for j in range(1, p2+1) :
                addr = f"(//div[@class='bama-checkbox-accordion__checkbox-container']/div/div/div[@class='bama-checkbox'])[{j}]"
                sub_elm = self.driver.find_element(By.XPATH, addr)
                self._highlight(sub_elm)

                if j==1 :
                    query_keyword = self._get_query_keyword(addr)
                    sub_elm = self.driver.find_element(By.XPATH, addr)


                parsed_sub = BS(sub_elm.get_attribute('innerHTML'), "html.parser")
                sub_text = parsed_sub.find("span", class_="bama-checkbox__text").get_text().strip()
                sub_name = parsed_sub.find("input", class_="bama-checkbox__input").get('name')

                sub_detail = {'name':sub_text, 'query_param':sub_name.split(sub_text)[1]}

                # Extract color codes if these below situations happen
                if text == self.exceptional_detail and self.cat == 'car':
                    sub_color = parsed_sub.find("span",
                                class_="bama-checkbox__color-circle").get('style').split(';')[0].split(':')[1].strip()
                    sub_detail['color_code'] = sub_color

                sub_details.append(sub_detail)

            items[text] = {'query_keyword':query_keyword, 'details':sub_details}

            self._highlight(elm)
            self.driver.execute_script("arguments[0].click();", elm)
            self.driver.implicitly_wait(5)
        
        return items

    def scrape(self, category) :
        self.cat = category
        self.driver.get(self._create_url(category))
        self.driver.implicitly_wait(10)

        all_details = self._get_brand_links(progress_bar=True)
        file_path = f"schemas/{self.prefix}/{category}.json"
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_details, f, ensure_ascii=False, indent=4)
        return file_path



if __name__ == '__main__' :
    bbs = BamaBrandScraper(highlight=True)
    path = bbs.scrape(category='car')
    print(path)

