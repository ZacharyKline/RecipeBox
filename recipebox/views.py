from django.shortcuts import render, HttpResponseRedirect, reverse
from recipebox.forms import RecipeItemAdd, AuthorAdd
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


def authoraddview(request):
    html = 'generic_add.html'
    if request.method == 'POST':
        form = AuthorAdd(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['name'],
                bio=data['bio']
            )
        return HttpResponseRedirect(reverse('homepage'))

    form = AuthorAdd()
    return render(request, html, {'form': form})


def recipeaddview(request):
    html = 'generic_add.html'
    if request.method == 'POST':
        form = RecipeItemAdd(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))
    form = RecipeItemAdd()
    return render(request, html, {'form': form})
