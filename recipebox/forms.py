from django import forms
from recipebox.models import Recipe


class AuthorAdd(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)


class RecipeItemAdd(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['author', 'title', 'description', 'time_req', 'instructions']


class StaffRecipeAdd(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['author', 'title', 'description', 'time_req', 'instructions']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
