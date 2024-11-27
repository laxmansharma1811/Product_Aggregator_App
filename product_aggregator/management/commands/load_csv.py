import csv
import re
from django.core.management.base import BaseCommand
from product_aggregator.models import DarazProduct, AmazonProduct

class Command(BaseCommand):
    help = 'Load product data from CSV files'

    def clean_price(self, price):
        """Remove non-numeric characters and convert to decimal."""
        cleaned_price = re.sub(r'[^\d.]', '', price)
        try:
            return float(cleaned_price)  # Convert to a float
        except ValueError:
            return None  # Handle invalid price formats gracefully

    def clean_rating(self, rating):
        """Extract numeric rating from strings like '4.1 out of 5 stars' or '76 Ratings'."""
        match = re.search(r'(\d+(\.\d+)?)', rating)
        if match:
            return float(match.group(1))  # Extract the first numeric value
        return None

    def handle(self, *args, **kwargs):
        # Load Daraz CSV
        try:
            with open('data/daraz.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    price = self.clean_price(row['Product Price'])
                    actual_price = self.clean_price(row.get('Actual_price', '0'))
                    rating = self.clean_rating(row.get('Rating', ''))
                    if price is not None:
                        DarazProduct.objects.create(
                            url=row['Product URL'],
                            name=row['Product Name'],
                            price=price,
                            actual_price=actual_price,
                            rating=rating,
                            color=row.get('color', None),
                        )
            self.stdout.write(self.style.SUCCESS('Daraz products loaded successfully!'))
        except FileNotFoundError:
            self.stderr.write('Daraz CSV file not found.')
        except Exception as e:
            self.stderr.write(f"Error loading Daraz CSV: {e}")

        # Load Amazon CSV
        try:
            with open('data/amazon.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    price = self.clean_price(row['Product Price'])
                    rating = self.clean_rating(row.get('Rating', ''))
                    if price is not None:
                        AmazonProduct.objects.create(
                            url=row['Product URL'],
                            name=row['Product Name'],
                            price=price,
                            rating=rating,
                            reviews=row.get('Number of reviews', None),
                            manufacturer=row.get('Manufacturer', None),
                            asin=row.get('ASIN', None),
                        )
            self.stdout.write(self.style.SUCCESS('Amazon products loaded successfully!'))
        except FileNotFoundError:
            self.stderr.write('Amazon CSV file not found.')
        except Exception as e:
            self.stderr.write(f"Error loading Amazon CSV: {e}")
