import requests
from bs4 import BeautifulSoup
import csv
def download_img(url):
    pass

def parse_price(price_text):
    price = price_text.replace(".","")
    price = price.replace("₫","")
    return price
def get_soup(url):
    URL = url
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def get_more_detail(url):
    soup_detail = get_soup(url)
    content = soup_detail.find("section",class_="section mt-0 mb-lg-4 mb-3 mb-sm-0")
    descriptions = content.find("div",class_="product-summary").find_all("li")
    rslt = ""
    for des in descriptions:
        rslt += "‣ "+ des.text + "\n"
    return rslt


def get_products_detail(url,category):
    soup = get_soup(url)
    products = soup.find("section",class_="section wrap_background").find_all("div",class_="item_product_main")
    print(len(products))
    data =  []
    cate = category
    for product in products:
        name = product.find("h3",class_ ="product-name").text
        url_detail =  "https://gymstore.vn" + product.find("h3",class_ ="product-name").find("a")['href']
        try: 
            description = get_more_detail(url_detail)
            img = "https:" + product.find("img",class_ = "product-thumbnail__img product-thumbnail__img--primary")['src']
            price = product.find("div",class_ = "price-box").find("span",class_="compare-price").text
            price = parse_price(price)
        except:
            description = ""
            img = "https:" + product.find("img",class_ = "product-thumbnail__img")['src']
            price = None      
            
        price_sale = product.find("div",class_ = "price-box").find("span",class_="price").text  
        price_sale = parse_price(price_sale)
        slug = product.find("h3",class_ ="product-name").find("a")['href'][1:]
        data.append([name,description,img,price,price_sale,slug,category])
        print("Finally crawl product:", name)
    return data


def get_products_pages(url,cate):
    data_ = []
    for i in range(1,5):
        url_ = url + "?q=collections:177279&page=" + str(i) + "&view=grid"
        print("Crawling page",i,url_)
        data = get_products_detail(url_,cate)
        data_.append(data)
       
  
    p = r'C:\Users\Admin\OneDrive\Desktop\WebApp\GCloud\GymECommerce\data\whey-protein\1.csv'

    with open(p, 'w',  encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        #writer.writerow(headers)
        for data in data_:
            for row in data:
                writer.writerow(row)


def write_to_csv(data):
    p = r'C:\Users\Admin\OneDrive\Desktop\WebApp\GCloud\GymECommerce\data\whey-protein\1.csv'
    #headers = ['name','description','img','price','price_sale','slug','category']

    with open(p, 'w',  encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        #writer.writerow(headers)
        for row in data:
            writer.writerow(row)


#data_whey = get_products_detail("https://gymstore.vn/whey-protein","whey-protein")
#write_to_csv(data_whey)
get_products_pages("https://gymstore.vn/whey-protein","whey-protein")