from django_filters.rest_framework import (
    BooleanFilter, FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag
from users.models import User


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = ModelChoiceFilter(
        method='filter_author',
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == int(True) and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == int(True) and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset

    def filter_author(self, queryset, name, value):
        if value == 'me':
            value = self.request.user.username
        return queryset.filter(author=value)


class IngredientFilter(SearchFilter):
    search_param = 'name'
