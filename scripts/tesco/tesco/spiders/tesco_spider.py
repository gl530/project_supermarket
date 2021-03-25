import scrapy
import json
import pandas as pd

class ProductSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://www.tesco.com/groceries/en-GB/shop/pets/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/fresh-food/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/bakery/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/frozen-food/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/drinks/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/baby/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/household/all?page=1',
        'https://www.tesco.com/groceries/en-GB/shop/home-and-ents/all?page=1'

    ]

    def parse(self, response):
        category = response.css('h1.heading.query::text').get()

        for product in response.css('div.tile-content'):

            yield {
                'category': category,
                'name': product.css('a.ui__StyledLink-sc-18aswmp-0.hgdSSe::text').get(),
                'price': product.css('span.value::text').get(),
                'data-auto-id': product.attrib['data-auto-id'],
                'id': product.attrib['id']
            }
            print()

        next_page_url = response.css(
            'li.pagination-btn-holder a::attr(href)').getall()[-1]

        if next_page_url is not None:
            print(category, ' download completed')
            yield response.follow(next_page_url, callback=self.parse)


class ProductDetailsSpider(scrapy.Spider):
    name = "product_details"
    start_urls = []
    filename = '/Users/lawlokin/Documents/data_science/projects/supermarket/data/tesco_w_link.json'

    with open(filename) as f:
        products = json.load(f)

        for p in products:
            start_urls.append(
                'https://www.tesco.com/groceries/en-GB/products/'+p['data-auto-id'])

    def parse(self, response):

        yield{
            'url': response.url,
            'prod_msg': response.css('div.product-info-message-wrapper.hidden-small.hidden-medium-small-only ::text').getall(),
            'prod_promo': response.css('div.promotions-wrapper ::text').getall(),
            'name': response.xpath('//h1[@class="product-details-tile__title"]/text()').get(),
            'price': response.xpath('//span[@data-auto="price-value"]/text()').get(),
            'prod_desc': response.xpath('//div[@class="product-blocks"]').css('::text').getall()
        }

class MatchedProdDetailsSpider(ProductDetailsSpider):
    name = "matched_tesco_prod_details"
    links_filename = '/Users/lawlokin/Documents/data_science/projects/supermarket/data/processed/matched_prods_incl_discont.csv'    
    matched_df = pd.read_csv(links_filename, sep='|')
    start_urls = list(matched_df['tesco_link'])

