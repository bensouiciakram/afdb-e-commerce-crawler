import json 
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from afdb.items import AfdbItem
from scrapy import Request 
from scrapy.shell import inspect_response
from scrapy.http.response.html import HtmlResponse



class ProductsSpider(CrawlSpider):
    """
    A web crawler to extract product information from the AFDB e-commerce website.

    This spider uses CrawlSpider rules to navigate through product pages and extract
    detailed product data including title, brand, stock information, and technical specifications.

    Attributes:
        name (str): Identifier for the spider ('products')
        allowed_domains (list): Domain restriction for crawling ['afdb.fr']
        start_urls (list): Starting point(s) for crawling ['https://www.afdb.fr']
        rules (tuple): URL matching rules for discovering product pages
    """

    name = 'products'
    allowed_domains = ['afdb.fr']
    start_urls = ['https://www.afdb.fr']
    
    rules = (              # rule to extract the product url
        Rule(LinkExtractor(allow=[r'.html$','SKU'],deny=['INTERSHOP']), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """
        Main callback method for processing product pages.

        Filters URLs containing 'SKU' and initiates product data extraction.
        Constructs ItemLoader to populate product fields and triggers stock check request.

        Args:
            response (HtmlResponse): The response object from the crawled page

        Returns:
            Request: Stock API request with item loader in meta or None if not a product page
        """
        if not ('SKU' in response.url) :
            return
        loader = ItemLoader(AfdbItem(),response)
        loader.add_value('url',response.url)
        loader.add_css('title','h1 span[itemprop=name]::text')
        loader.add_css('brand','div.product-brand img::attr(title)')
        loader.add_css('image_urls','div.swiper-wrapper img::attr(src)')
        loader.add_css('description', 'div#ProductTabDescription div::text')
        loader.add_xpath('category','//li[contains(@class,"breadcrumbs-list")][position()>1]/a/text()')
        loader.add_value('sku',self.get_sku(response))
        loader.add_value('details',self.get_details(response))
        loader.add_xpath('variure','//label[contains(text(),"VARIURE")]//parent::div/text()')
        loader.add_xpath('finition','//label[contains(text(),"FINITION")]//parent::div/text()')
        loader.add_xpath('type','//label[contains(text(),"TYPE")]//parent::div/text()')
        stock_url = 'https://www.afdb.fr/INTERSHOP/web/WFS/AFDB-B2B-Site/fr_FR/-/EUR/IncludeProduct-GetStocks?SKUs={}&ShowMessage=true'
        yield Request(
            stock_url.format(loader._values.get('sku')[0]),
            meta ={
                'loader':loader
            },
            callback=self.get_stock

        )

    def get_stock(self,response:HtmlResponse):
        """
        Callback for handling stock information API response.

        Completes item loading process by adding stock data and yielding final product item.

        Args:
            response (HtmlResponse): JSON response containing stock information

        Returns:
            Item: Fully populated product item
        """
        loader = response.meta.get('loader')
        loader.add_value('stock',response.json()['results'][0]['views'][0]['result'][0]['message'])
        yield loader.load_item()
            
    def get_details(self,response:HtmlResponse) -> dict :
        """
        Extracts technical specifications from product attributes section.

        Args:
            response (HtmlResponse): Page response containing product details

        Returns:
            dict: Key-value pairs of product attributes from <dl> elements
        """
        return {
            sel.xpath('.//dt//text()').get():sel.xpath('.//dd//text()').get()
            for sel in response.xpath(
                '//dl[@class="ish-productAttributes"]'
            )
        }
            
    def get_sku(self,response:HtmlResponse) -> str:
        """
        Extracts SKU from structured data in page's JSON script tag.

        Args:
            response (HtmlResponse): Page response containing product schema data

        Returns:
            str: Product SKU identifier
        """
        return json.loads(
            response.xpath(
                '//script[@data-qa="structuredDataProductSEO"]/text()'
            ).get()
        )['sku']
