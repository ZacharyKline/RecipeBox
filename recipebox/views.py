from django.shortcuts import render, HttpResponseRedirect, reverse
from recipebox.forms import (
    RecipeItemAdd, AuthorAdd, LoginForm, StaffRecipeAdd, EditRecipeItem)
from recipebox.models import Recipe, Author
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    html = 'index.html'
    recipes = Recipe.objects.all()
    user_is_admin = request.user.is_staff
    return render(request, html, {
        'data': recipes,
        'user_is_admin': user_is_admin})


def recipe_view(request, id):
    recipe_html = 'recipes.html'
    recipe = Recipe.objects.filter(pk=id)
    user = request.user

    is_admin = user.is_staff
    user_is_author = False
    is_fav = False
    if user.is_authenticated:
        if not is_admin:
            author = Author.objects.get(user=user)
            user_is_author = author == recipe[0].author
            favorites = author.favorites.all()
            is_fav = recipe[0] in favorites
    return render(request, recipe_html, {
        'data': recipe,
        'is_admin': is_admin,
        'logged_in_is_author': user_is_author,
        'user': user,
        'is_fav': is_fav
    })


def author_view(request, id):
    author_html = 'authors.html'
    author = Author.objects.filter(id=id)
    recipes = Recipe.objects.filter(author=id)

    return render(request, author_html, {
        'data': author,
        'recipes': recipes,
    })


@login_required
def authoraddview(request):
    html = 'generic_add.html'
    if request.user.is_staff:
        if request.method == 'POST':
            form = AuthorAdd(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                u = User.objects.create_user(
                    username=data['username'],
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
def staffrecipeview(request):
    html = 'generic_add.html'
    if request.user.is_staff:
        author = Recipe.objects.all()
        if request.method == 'POST':
            form = StaffRecipeAdd(request.POST)
            form.save()
            return HttpResponseRedirect(reverse('homepage'))
        form = StaffRecipeAdd()
        return render(request, html, {'form': form, 'authors': author})
    return HttpResponseRedirect('/error')


@login_required
def edit_recipe(request, id):
    html = 'generic_add.html'

    instance = Recipe.objects.get(pk=id)

    is_admin = request.user.is_staff
    logged_in_is_author = False
    if not is_admin:
        logged_in_author = Author.objects.get(user=request.user)
        logged_in_is_author = logged_in_author.id == instance.author.id

    if not is_admin and not logged_in_is_author:
        return HttpResponseRedirect(reverse('homepage'))
    elif (request.method == 'POST'):
        form = EditRecipeItem(request.POST, instance=instance)
        form.save()
        return HttpResponseRedirect(reverse('recipes_page', args=(id,)))

    form = EditRecipeItem(instance=instance)
    return render(request, html, {'form': form})


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
                    request.GET.get('next', reverse('homepage')))
    form = LoginForm()
    return render(request, html, {'form': form})


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))


def errorpage(request):
    html = 'error.html'
    return render(request, html)


@login_required
def my_favorites_view(request):
    html = 'favorites.html'
    user = request.user
    if user.is_staff:
        HttpResponseRedirect(reverse('homepage'))
    author = Author.objects.get(user=user)
    my_favorites = author.favorites.all()

    return render(request, html, {'my_favorites': my_favorites})


@login_required
def add_favorite(request, id):
    user = request.user
    if user.is_staff:
        HttpResponseRedirect(reverse('recipes_page', args=(id,)))
    author = Author.objects.get(user=user)
    recipe = Recipe.objects.get(pk=id)
    author.favorites.add(recipe)
    return HttpResponseRedirect(reverse('recipes_page', args=(id,)))


@login_required
def remove_favorite(request, id):
    user = request.user
    if user.is_staff:
        HttpResponseRedirect(reverse('recipes_page', args=(id,)))
    author = Author.objects.get(user=user)
    recipe = Recipe.objects.get(pk=id)
    author.favorites.remove(recipe)
    return HttpResponseRedirect(reverse('recipes_page', args=(id,)))
