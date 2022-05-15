from rest_framework.serializers import ValidationError

from foodgram.settings import (
    INGREDIENT_AMOUNT_FIELD_ERROR, INGREDIENT_AMOUNT_VALIDATION_ERROR,
    INGREDIENT_FIELD_ERROR, INGREDIENT_VALIDATION_ERROR,
    UNIQUE_INGREDIENT_VALIDATION_ERROR
)
from recipes.models import Ingredient


def validate_ingredient_amounts(ingredients):
    if not ingredients:
        raise ValidationError(INGREDIENT_FIELD_ERROR)
    unique_ingridients_list = []
    for ingredient in ingredients:
        if ingredient.get('amount') is None:
            raise ValidationError(INGREDIENT_AMOUNT_FIELD_ERROR)
        if ingredient.get('amount') < 1:
            raise ValidationError(INGREDIENT_AMOUNT_VALIDATION_ERROR)
        ingredient_id = ingredient.get('id')
        if ingredient_id in unique_ingridients_list:
            raise ValidationError(UNIQUE_INGREDIENT_VALIDATION_ERROR)
        unique_ingridients_list.append(ingredient_id)
        if not Ingredient.objects.filter(id=ingredient_id).exists():
            raise ValidationError(INGREDIENT_VALIDATION_ERROR)
