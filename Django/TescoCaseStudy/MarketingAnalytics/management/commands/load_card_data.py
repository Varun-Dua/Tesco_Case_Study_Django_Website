from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from MarketingAnalytics.models import Cards


ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the pet data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from content_train_TESCO.csv into our Card mode"

    def handle(self, *args, **options):
        if Cards.objects.exists():
            print('Card data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Loading card data for cards available to click")
        for row in DictReader(open('./content_train_TESCO.csv')):
            card = Cards()
            card.customer = row['customer']
            card.content_1 = row['content_1']
            card.content_2 = row['content_2']
            card.content_3 = row['content_3']
            card.content_4 = row['content_4']
            card.content_5 = row['content_5']
            card.content_6 = row['content_6']
            card.content_7 = row['content_7']
            card.content_8 = row['content_8']
            card.content_9 = row['content_9']
            card.express_no_transactions = row['express_no_transactions']
            card.express_total_spend = row['express_total_spend']
            card.metro_no_transactions = row['metro_no_transactions']
            card.metro_total_spend = row['metro_total_spend']
            card.superstore_no_transactions = row['superstore_no_transactions']
            card.superstore_total_spend = row['superstore_total_spend']
            card.extra_no_transactions = row['extra_no_transactions']
            card.extra_total_spend = row['extra_total_spend']
            card.fandf_no_transactions = row['fandf_no_transactions']
            card.fandf_total_spend = row['fandf_total_spend']
            card.petrol_no_transactions = row['petrol_no_transactions']
            card.petrol_total_spend = row['petrol_total_spend']
            card.direct_no_transactions = row['direct_no_transactions']
            card.direct_total_spend = row['direct_total_spend']
            card.gender = row['gender']
            card.affluency = row['affluency']
            card.county = row['county']

            card.save()
