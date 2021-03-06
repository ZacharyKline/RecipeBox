"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipebox import views
from recipebox.models import Author, Recipe
from django.conf import settings
from django.conf.urls.static import static

admin.site.register(Author)
admin.site.register(Recipe)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('recipes/<int:id>/', views.recipe_view, name='recipes_page'),
    path('authors/<int:id>/', views.author_view, name='authors_page'),
    path('addrecipe/', views.recipeaddview, name='recipe_add_page'),
    path('addauthor/', views.authoraddview, name='author_add_page'),
    path('login/', views.loginview, name='login_page'),
    path('logout/', views.logoutview, name='logout_page'),
    path('error/', views.errorpage, name='error_page'),
    path('staffrecipeadd/', views.staffrecipeview,
         name='staff_recipe_add_page')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
