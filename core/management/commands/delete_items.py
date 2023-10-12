from core.models import Product 
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        items = Product.objects.all()
        items.delete()
        print("Remove all item successfully")
    