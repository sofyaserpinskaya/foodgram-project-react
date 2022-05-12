from rest_framework import serializers

from recipes.models import Ingredient


INGREDIENT_FIELD_ERROR = 'Поле ingredients обязательно.'
INGREDIENT_VALIDATION_ERROR = 'Такого ингредиента нет в БД.'
INGREDIENT_AMOUNT_VALIDATION_ERROR = 'Укажите количество ингредиентов.'


def validate_ingredient_amounts(ingredients):
    if not ingredients:
        raise serializers.ValidationError(INGREDIENT_FIELD_ERROR)
    for ingredient in ingredients:
        if not Ingredient.objects.filter(id=ingredient.get('id')).exists():
            raise serializers.ValidationError(INGREDIENT_VALIDATION_ERROR)
        if ingredient.get('amount') is None:
            raise serializers.ValidationError(
                INGREDIENT_AMOUNT_VALIDATION_ERROR
            )
