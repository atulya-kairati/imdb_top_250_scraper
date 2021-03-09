import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        # Order of rules matters
        # 1. for handling all movie links in a page.
        # Never set callback to "parse" => it will break the crawl spider
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True),
        # 2. for Pagination
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="lister-page-next next-page"])[1]'))
    )

    def parse_item(self, response):
        name = response.xpath('//div[@class="title_wrapper"]/h1/text()').get()
        year = response.xpath('//div[@class="title_wrapper"]/h1/span/a/text()').get()
        duration = response.xpath('normalize-space(//div[@class="title_wrapper"]/div[@class="subtext"]/time/text())').get()
        rating = response.xpath('//span[@itemprop="ratingValue"]/text()').get()
        genre = response.xpath('//div[@class="title_wrapper"]/div[@class="subtext"]/a[1]/text()').get()
        movie_url = response.url

        yield {
            'name': name,
            'year': year,
            'duration': duration,
            'rating': rating,
            'genre': genre,
            'movie_url': movie_url
        }
