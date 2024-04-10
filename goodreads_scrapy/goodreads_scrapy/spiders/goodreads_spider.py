import scrapy
from goodreads_scrapy.items import GoodreadsBookItem

class GoodreadsSpider(scrapy.Spider):
    name = 'goodreads'
    allowed_domains = ['goodreads.com']
    start_urls = [f'https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page={i}' for i in range(1, 6)]

    def parse(self, response):
        books = response.xpath('//tr[@itemtype="http://schema.org/Book"]')
        for book in books:
            item = GoodreadsBookItem()
            """
            with open('response.html', 'wb') as f:
                f.write(response.body)
            """
            item['title'] = book.xpath('.//a[contains(@class, "bookTitle")]/span/text()').get().strip()
            item['author'] = book.xpath('.//a[contains(@class, "authorName")]/span/text()').get().strip()
            item['score'] = book.xpath("//a[contains(@onclick, 'score_explanation')]/text()").get()[7:]
            item['url'] = book.xpath('.//a[contains(@class, "bookTitle")]/@href').get()
            book_url = response.urljoin(item['url'])
            request = scrapy.Request(book_url, callback=self.parse_book_details)
            request.meta['item'] = item
            yield request

    def parse_book_details(self, response):
        item = response.meta['item']
        """
        with open('response.html', 'wb') as f:
            f.write(response.body)
        """
        details_span = response.xpath("//span[@class='Text Text__body3']")
        item['pages'] = details_span.xpath(".//p[@data-testid='pagesFormat']/text()").get().split(' ')[0]
        item['year'] = details_span.xpath(".//p[@data-testid='publicationInfo']/text()").get().split(',')[-1].strip()
        item['genre'] = response.xpath('//a[contains(@href, "/genres/")]/span/text()').getall()#response.xpath("//span[@class='BookPageMetadataSection__genreButton']/span/text()").getall()
        item['desc'] = response.xpath("//span[@class='Formatted']/text()").get() 
        item['reviews'] = response.xpath('//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[2]/a/div[2]/div/span[2]/text()').get()#response.xpath("//span[@data-testid='reviewsCount']/span/text()").get().split()[0]
        yield item
