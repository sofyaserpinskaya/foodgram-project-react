from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

from .serializers import RecipeShortSerializer
from recipes.models import Recipe


NO_RECIPE = 'Такого рецепта нет в списке.'
RECIPE_ALREADY_IN = 'Рецепт уже добавлен в список.'


def create_delete_recipes_list(request, pk, model):
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == 'POST':
        try:
            obj = model.objects.create(
                user=request.user, recipe=recipe
            )
            serializer = RecipeShortSerializer(recipe)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )
        except IntegrityError:
            return Response(
                {'errors': RECIPE_ALREADY_IN},
                status=status.HTTP_400_BAD_REQUEST
            )
    obj = model.objects.filter(
        user=request.user, recipe=recipe
    )
    if obj:
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'errors': NO_RECIPE}, status=status.HTTP_400_BAD_REQUEST
    )
