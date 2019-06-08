from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
#from django.contrib.auth.models import User
from authapp.models import ShopUser

import json, os


JSON_PATH = 'mainapp/json'


def loadFromJSON(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        categories = loadFromJSON('categories')

        ProductCategory.objects. all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = loadFromJSON('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        super_user = ShopUser.objects.create_superuser('django', 'paveldudkov003@gmail.com', 'geekbrains', age=31)


