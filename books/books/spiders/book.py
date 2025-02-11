import scrapy


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books_links = response.css("article.product_pod h3 a::attr(href)").getall()
        for book_link in books_links:
            yield response.follow(book_link, callback=self.parse_book)

        next_page_link = response.css("li.next a::attr(href)").get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse)

    def parse_book(self, response):
        pass