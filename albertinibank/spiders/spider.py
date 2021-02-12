import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import AlbertinibankItem
from itemloaders.processors import TakeFirst


class AlbertinibankSpider(scrapy.Spider):
	name = 'albertinibank'
	start_urls = ['https://www.albertinibank.it/it']

	def parse(self, response):
		post_links = response.xpath('//span[@class="link"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/span/text()').get()
		description = response.xpath('//div[@class="header-content"]//text()[normalize-space()]|//div[@class="col-md-9 col-md-offset-3"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]//text()').get()
		if date:
			date = re.findall(r"(\d+-[a-zA-Z]+-\d+)", date)[0]

		item = ItemLoader(item=AlbertinibankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
