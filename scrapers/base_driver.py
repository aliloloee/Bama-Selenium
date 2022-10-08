from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time



class DynamicDriverSetUp() :
    def __init__(self, *args, **kwargs) :
        self.base_url = 'http://bama.ir/'
        self.allowed_categories = ['car', 'motorcycle']
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)'
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                    options=self._create_driver_options())

    def _create_driver_options(self) :
        chrome_options = ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("—disable-gpu")
        chrome_options.add_argument("--window-size=1150,630")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        return chrome_options

    def _end_driver(self) :
        self.driver.close()


class DriverSetUp() :
    def __init__(self, highlight, *args, **kwargs) :
        self.base_url = 'http://bama.ir/'
        self.allowed_categories = ['car', 'motorcycle']
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)'
        self._create_highlight_options(highlight)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                    options=self._create_driver_options())

    def _create_driver_options(self) :
        chrome_options = ChromeOptions()
        if not self.highlight :
            chrome_options.headless = True
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("—disable-gpu")
        chrome_options.add_argument("--window-size=1150,630")
        # chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        return chrome_options

    def _create_highlight_options(self, highlight) :
        self.effect_time = 2
        self.color = "blue"
        self.border = 5
        self.temp_style = "border: {0}px solid {1};".format(self.border, self.color)
        self.highlight = highlight

    def _highlight(self, element):
        if self.highlight :
            original_style = element.get_attribute('style')
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                    element, self.temp_style)
            time.sleep(self.effect_time)
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                    element, original_style)

    def _progressBar(self, iterable, prefix = '', suffix = '', decimals = 1,
                    length = 100, fill = '█', printEnd = "\r"):
        total = len(iterable)
        # Progress Bar Printing Function
        def printProgressBar (iteration):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Initial Call
        printProgressBar(0)
        # Update Progress Bar
        for i, item in enumerate(iterable):
            yield item
            printProgressBar(i + 1)
        # Print New Line on Complete
        print()

    def _end_driver(self) :
        self.driver.close()