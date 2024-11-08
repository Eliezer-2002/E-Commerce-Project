import pandas as pd
from django.core.files import File
from django.core.management.base import BaseCommand
from shop.models import Products  # Make sure 'your_app' is replaced with your actual app name
import os
import datetime
from django.utils.text import slugify
import uuid
def getFileName(filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{now_time}{filename}"
    return os.path.join('uploads/', new_filename)

class Command(BaseCommand):
    help = 'Upload products from CSV'

    def handle(self, *args, **kwargs):
        data = pd.read_csv('data/products.csv')
        
        for _, row in data.iterrows():
            now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"{now_time}_{os.path.basename(row['image_path'])}"

            product = Products(
                category_id=row['category_id'],  # Ensure category_id is provided in CSV
                name=row['name'],
                vendor=row['vendor'],
                quantity=row['quantity'],
                original_price=row['original_price'],
                selling_price=row['selling_price'],
                description=row['description'],
                status=row['status'],
                trending=row['trending']
            )

            # Handle image upload
            if os.path.exists(row['image_path']):
                with open(row['image_path'], 'rb') as img_file:
                    product.product_image.save(new_filename, File(img_file), save=False)

            # Handle slug creation
            product.slug = f"{slugify(row['name'])}-{uuid.uuid4().hex[:8]}"

            # Save the product instance
            product.save()

        self.stdout.write(self.style.SUCCESS('Data uploaded successfully!'))