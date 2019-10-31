from django import forms
from recipebox.models import Recipe


class AuthorAdd(forms.Form):
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)


class RecipeItemAdd(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['author', 'title', 'description', 'time_req', 'instructions']
