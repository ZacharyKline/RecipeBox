from django.shortcuts import render, HttpResponseRedirect, reverse
from recipebox.forms import RecipeItemAdd, AuthorAdd, LoginForm
from recipebox.models import Recipe, Author
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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


@login_required
def authoraddview(request):
    html = 'generic_add.html'
    if request.user.is_staff:
        if request.method == 'POST':
            form = AuthorAdd(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                u = User.objects.create_user(
                    username=data['name'],
                    password=data['password']
                )
                Author.objects.create(
                    user=u,
                    name=data['name'],
                    bio=data['bio'],

                )
            return HttpResponseRedirect(reverse('homepage'))

        form = AuthorAdd()
        return render(request, html, {'form': form})
    return HttpResponseRedirect('/error')


@login_required
def recipeaddview(request):
    html = 'generic_add.html'
    if request.method == 'POST':
        form = RecipeItemAdd(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))
    form = RecipeItemAdd()
    return render(request, html, {'form': form})


def loginview(request):
    html = 'generic_add.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, html, {'form': form})


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def errorpage(request):
    html = 'error.html'
    return render(request, html)
