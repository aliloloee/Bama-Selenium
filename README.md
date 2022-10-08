<h2>What is this project about ?</h2>

<p><strong>Bama.ir</strong> is a website that sells cars and motorcycles online. Scraping this website can be a little tricky using libraries like beautifulsoup alone, since the website is not static and <code>uses javascript</code> to load many of the filters and items.</p>

<p>This project utilizes<code>selenium</code> for scraping. Though this tool is mainly for testing purposes, but it can also be used in scraping projects.</p>

<h2>How to use :</h2>

<p>Simply, clone the project, then execute <code>pip install -r requirements.txt</code>, and run the files <code>test_dynamic.py</code> and <code>test_static.py</code></p>

<p><code>test_dynamic.py</code> utilizes the <code>BamaScraper</code> class to scrape cars or motorcycles according to keyword arguments you provide for a method of this class : <code>scrape</code></p>

<p><code>test_static.py</code> utilizes multiple classes to scrape brands, cities and other details of the products available on this website. All these classes produce a <code>json file (in utf-8 format)</code> of scraped objects. You can instantiate these class with a parameter<code>highlight</code>. If it is set to True, you will observe the objects that are being scraped in an open browser, however in this mode scraping all objects takes too much time(Consider this mode as a mode to observe if selenium is doing it's work properly). Set this parameter to False to let selenium do it's job in <code>headless mode</code> without highlighting and the final file will be produced much faster.</p>


<h3>Github address</h3>
<a href="https://github.com/aliloloee">github.com/aliloloee</a>


