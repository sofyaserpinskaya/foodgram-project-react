import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


def ingredient_create(row):
    Ingredient.objects.get_or_create(
        name=row[0],
        measurement_unit=row[1],
    )


action = {
    "ingredients.csv": ingredient_create,
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = '/Users/sofyaserpinskaya/Dev/foodgram-project-react/data/'
        for key in action.keys():
            with open(path + key, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    action[key](row)
