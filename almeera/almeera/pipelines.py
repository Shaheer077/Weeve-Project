# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
#
# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# from .items import ProductItem,SubcategoryItem,CategoryItem
#
# class AlmeeraPipeline():
#     products=[]
#     subcatagories=[]
#     def process_item(self, item, spider):
#         if isinstance(item, ProductItem):
#             print("Product item",item)
#             self.products.append(item)
#         elif isinstance(item, SubcategoryItem):
#             print("Subcategory item",item)
#             item['Products']=self.products
#         elif isinstance(item,CategoryItem):
#             print("Category item",item)
#             item['Subcategories']=self.subcatagories
#
#         return item
