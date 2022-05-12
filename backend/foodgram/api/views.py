from django.http import HttpResponse

from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .filters import RecipeFilter
from .pagination import PageLimitPagination
from .permissions import IsAuthenticatedAuthorOrReadOnly
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer
)
from .utils import create_delete_recipes_list
from recipes.models import (
    Tag, Ingredient, Recipe, IngredientAmount, Favorite,
    ShoppingCart
)


FOODGRAM = '\n________\nFoodgram'
SHOPPING_CART = (
    'Привет, {username}!\nВот твой список покупок:\n'
    '________________________\n\n'
)


class TagViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedAuthorOrReadOnly,)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args, **kwargs)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return create_delete_recipes_list(request, pk, Favorite)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return create_delete_recipes_list(request, pk, ShoppingCart)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shopping_dict = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__in=request.user.shopping_cart.values('recipe')
        ).select_related('ingredient')
        for obj in ingredients:
            ingredient = obj.ingredient.name
            if ingredient not in shopping_dict:
                shopping_dict[ingredient] = {
                    'measurement_unit': obj.ingredient.measurement_unit,
                    'amount': obj.amount
                }
            else:
                shopping_dict[ingredient]['amount'] += obj.amount
        download_cart = SHOPPING_CART.format(username=request.user.username)
        for ingredient in shopping_dict:
            download_cart += (
                f'{ingredient} '
                f'({shopping_dict[ingredient]["measurement_unit"]}) '
                f'- {shopping_dict[ingredient]["amount"]}\n'
            )
        download_cart += FOODGRAM
        response = HttpResponse(
            download_cart,
            content_type='text/plain;charset=UTF-8',
        )
        response['Content-Disposition'] = (
            'attachment;'
            'filename="shopping_cart.txt"'
        )
        return response
