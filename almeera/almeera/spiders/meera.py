import scrapy
from ..items import ProductItem, SubcategoryItem, CategoryItem
import requests
import os

class MeeraSpider(scrapy.Spider):
    name = "meera"
    allowed_domains = ["almeera.online"]
    start_urls = ["http://almeera.online/"]
    prod_item=ProductItem()
    sub_item=SubcategoryItem()
    cat_item=CategoryItem()
    def parse(self, response):
        data = response.css("div.content")
        cat = data.css("ul.subcategory-view-icons.subcategory-list.grid-list.clearfix")
        cats = cat.css("li")
        Cate_href = cats.css("a::attr('href')").getall()
        Cate_Name = cats.css("span.subcategory-name::text").getall()
        Cate_IMG = cats.css("img::attr('src')").getall()
        Cate_href = ["https://almeera.online/" + x for x in Cate_href]
        for i in range(len(Cate_href)):
            self.cat_item['CategoryTitle'] = Cate_Name[i]
            self.cat_item['CategoryImageURL'] = "https:" + Cate_IMG[i]
            folder_name = "cate_Image"
            ImgUrl= "https:" + Cate_IMG[i]
            file_name = os.path.basename(ImgUrl)
            local_filename = os.path.join(folder_name, file_name)
            resp = requests.get(ImgUrl)
            if resp.status_code == 200:
                # If the request was successful, save the image to the "cate_Image" folder
                with open(local_filename, 'wb') as file:
                    file.write(resp.content)
            yield scrapy.Request(url=Cate_href[i], callback=self.parse_SubCate)

        
    def parse_SubCate(self, response):
        data = response.css("div.content")
        cat = data.css("ul.subcategory-view-icons.subcategory-list.grid-list.clearfix")
        cats = cat.css("li")
        SubCate_href = cats.css("a::attr('href')").getall()
        SubCate_Name = cats.css("span.subcategory-name::text").getall()
        SubCate_href = ["https://almeera.online/" + x for x in SubCate_href]
        for i in range(len(SubCate_href)):
            self.sub_item = SubcategoryItem()
            self.sub_item['SubcategoryTitle'] = SubCate_Name[i]
            yield scrapy.Request(url=SubCate_href[i], callback=self.parse_product)
        

    def parse_product(self, response):
        data = response.css("div.products")
        cat = data.css("ul.products-grid.grid-list")
        cats = cat.css("li")
        Product_href = cats.css("a::attr('href')").getall()
        for Products in Product_href:
            Products = "https://almeera.online/" + Products + "#product-details-tab-specification"
            yield scrapy.Request(url=Products, callback=self.parse_Final)
         


    def parse_Final(self, response):
        data = response.css("div.list-container")
        value = data.css("li.identifier.product-sku")
        SKU = value.css("span.value::text").get()
        self.prod_item['ItemTitle']=data.css("h1.fn.title::text").get()
        self.prod_item['ItemImageURL']=data.css("img::attr('src')").get()
        folder_name = "Prod_Image"
        ImgUrl = "https:" + data.css("img::attr('src')").get()
        file_name = os.path.basename(ImgUrl)
        local_filename = os.path.join(folder_name, file_name)
        resp = requests.get(ImgUrl)
        if resp.status_code == 200:
            # If the request was successful, save the image to the "cate_Image" folder
            with open(local_filename, 'wb') as file:
                file.write(resp.content)
        self.prod_item['ItemPrice']=data.css("span.price.product-price::text").get()
        self.prod_item['ItemBarcode']=SKU
        self.sub_item['Products']=self.prod_item
        self.cat_item['Subcategories']=self.sub_item
        yield self.cat_item
        try:
            page=response.css('ul.pagination.grid-list')
            next=page.css('li.item active next-page')
            next_page_url = next.css('a::attr(href)').get()
            print("got next page url",next_page_url)
            if next_page_url:
                yield scrapy.Request(url="https://almeera.online/"+next_page_url, callback=self.parse_Final)
        except:
            pass

