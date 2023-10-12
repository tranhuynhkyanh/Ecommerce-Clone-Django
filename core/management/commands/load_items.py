from core.models import Product,Vendor,ProductInventory,Category,Tag
import csv
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding="utf-8") as f:
            reader = csv.reader(f,delimiter = ',')
            for row in reader:
                # Tạo một đối tượng `MyModel` mới
                if row[3] == None or row[3] == '':
                    price_ = row[4]
                    price_discount = None
                else: 
                    price_ =  row[3]
                    price_discount = row[4]
                product = Product.objects.create(
                    title = row[0],
                    category = Category.objects.get(title="Supplements"),
                    description =row[1] ,
                    price =price_discount ,
                    old_price = price_,
                    image = None,
                    image_url = row[2],
                    product_status = "Draft",
                    status = True,
                    in_stock = True ,
                    featured = True ,
                    digital = True ,
                    vendor = Vendor.objects.get(title="AdminShop"))
                ProductInventory.objects.create(product=product,quantity =10)
                print("Create product:" ,row[0])
            
#python manage.py load_items --path C:/Users/Admin/OneDrive/Desktop/WebApp/GCloud/GymECommerce/data/whey-protein/1.csv