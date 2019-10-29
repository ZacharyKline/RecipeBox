from django.shortcuts import render

from recipebox.models import Recipe, Author


def index(request):
    html = 'index.html'

    recipes = Recipe.objects.all()

    return render(request, html, {'data': recipes})


def recipe_view(request, id):
    recipe_html = 'recipes.html'
    recipe = Recipe.objects.filter(id=id)

    return render(request, recipe_html, {'data': recipe})


def author_view(request, id):
    author_html = 'authors.html'
    author = Author.objects.filter(id=id)
    recipes = Recipe.objects.filter(author=id)

    return render(request, author_html, {'data': author, 'recipes': recipes})
