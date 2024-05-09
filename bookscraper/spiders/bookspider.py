import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    #To specify which domains we allow the spider to scrape as the website can contain links to external websites.
    start_urls = ["https://books.toscrape.com"]
    #Can contain multiple urls

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            yield{
                'name': book.css('h3 a::text').get() ,
                'price': book.css('div.product_price p.price_color::text').get(),
                'url' : book.css('h3 a').attrib['href']
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page: 
                next_page_url = 'https://books.toscrape.com/'+next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/'+next_page
            yield response.follow(next_page_url, callback=self.parse)
            