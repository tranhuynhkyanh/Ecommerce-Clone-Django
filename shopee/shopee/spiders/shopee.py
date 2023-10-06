import scrapy

class ShopeeSpider(scrapy.Spider):
    name = "shopee"
    start_urls = ["https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567"]

    def parse(self, response):
        # Lấy danh sách sản phẩm
        products = response.css(".col-xs-2-4 shopee-search-item-result__item")

        # Lặp qua danh sách sản phẩm
        for product in products:
            # Lấy dữ liệu sản phẩm
            name = product.css(".OspxFR").text
            price = product.css(".product-price").text
            image_url = product.css(".PiYBEi KbUcCB").get("src")

            # Lưu dữ liệu sản phẩm
            yield {
                "name": name,
                "price": price,
                "image_url": image_url
            }

        # Di chuyển đến trang tiếp theo
        next_url = response.css(".next").attrib["href"]
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)