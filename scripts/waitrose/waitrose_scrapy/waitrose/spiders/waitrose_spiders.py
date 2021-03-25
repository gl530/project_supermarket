import scrapy
import pandas as pd
import re
import csv
import sys
from datetime import date

class ProdDetailsSpider(scrapy.Spider):

    name = "waitrose_prod_details"
    filename = '/Users/lawlokin/Documents/data_science/projects/supermarket/data/processed/matched_prods_incl_discont.csv'
    prod_mapping = pd.read_csv(filename, sep='|')
    wt_link = list(prod_mapping['wt_link'])
    start_urls = wt_link

    def parse(self, response):
        link = response.url
        name = response.css('span.name___30fwb ::text').get()
        size = response.css('span.size___2HSwr.sizeMessage___3o5Ri ::text').get()
        price = response.xpath('//span[@data-test="product-pod-price"]/span/text()').get()
        prod_msg = response.xpath('//div[@data-test="conflict-message"]').css('.message___3RyQU ::text').get()
        offer = response.css('.promotions___2ZvQR ::text').getall()
        prod_details = response.css('div.col-xs-12of12.col-md-8of12 ::text').getall()

        filename = '/Users/lawlokin/Documents/data_science/projects/supermarket/data/processed/matched_waitrose_prod_details.csv'

        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([link, name, size, price, prod_msg, offer, prod_details])
            f.close()