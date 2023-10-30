# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    ItemTitle = scrapy.Field()
    ItemImageURL = scrapy.Field()
    ItemPrice = scrapy.Field()
    ItemBarcode = scrapy.Field()


class SubcategoryItem(scrapy.Item):
    SubcategoryTitle = scrapy.Field()
    Products = scrapy.Field(serializer=ProductItem)


class CategoryItem(scrapy.Item):
    CategoryTitle = scrapy.Field()
    CategoryImageURL = scrapy.Field()
    Subcategories = scrapy.Field(serializer=SubcategoryItem)
