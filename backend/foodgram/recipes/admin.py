from django.contrib import admin

from .models import (
    Favorite, Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'total_favorited')
    list_filter = ('author', 'name', 'tags')

    def total_favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    total_favorited.short_description = 'Добавлен в избранное'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart)
