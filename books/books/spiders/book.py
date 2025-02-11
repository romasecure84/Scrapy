import scrapy
from ..items import BookItem

number_dict = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}


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
        book = BookItem()

        book["name"] = response.css("div.product_main h1::text").get()

        book["price_excl_tax"] = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td[1]/text()').get()
        book["price_incl_tax"] = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td[1]/text()').get()
        book["upc"] = response.xpath('//th[text()="UPC"]/following-sibling::td[1]/text()').get()
        book["availability"] = response.xpath('//th[text()="Availability"]/following-sibling::td[1]/text()').get()
        book["tax"] = response.xpath('//th[text()="Tax"]/following-sibling::td[1]/text()').get()

        category_children = response.xpath('//ul[@class="breadcrumb"]/child::*')
        book["category"] = category_children[2].css("a::text").get()

        star_tag = response.css('p.star-rating')
        class_name_string = star_tag.attrib["class"]
        stars = class_name_string.split(" ")[-1]
        book["stars"] = number_dict[stars]

        book["image_url"] = 'https://books.toscrape.com' + response.css("div.active img").attrib["src"][5:]

        yield book