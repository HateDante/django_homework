from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'cottage_cheese_casserole': {
        'творог, пачка': 2,
        'яйца, шт': 3,
        'сахар, ст.л.': 1,
        'сметана, ст.л.': 1,
        'корица, шеп': 1,
    }
    # можете добавить свои рецепты ;)
}


# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
def omlet(request):
    context = print_recipe('omlet', request)
    return render(request, 'calculator/index.html', context)


def pasta(request):
    context = print_recipe('pasta', request)
    return render(request, 'calculator/index.html', context)


def buter(request):
    context = print_recipe('buter', request)
    return render(request, 'calculator/index.html', context)


def cottage_cheese_casserole(request):
    context = print_recipe('cottage_cheese_casserole', request)
    return render(request, 'calculator/index.html', context)


def print_recipe(recipe_name, request):
    servings = get_servings(request)
    recipes_book = DATA.copy()
    recipe_ingredients = recipes_book.get(recipe_name)
    multiply_receipt(recipe_ingredients, servings)
    context = {
        'recipe': recipe_ingredients
    }
    return context


def get_servings(request):
    servings = request.GET.get('servings')
    if servings is not None:
        servings = int(servings)
    return servings


def multiply_receipt(recipe, servings):
    if servings is not None:
        for item, value in recipe.items():
            recipe[item] = value * servings
