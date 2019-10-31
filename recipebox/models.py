"""
Author Model:
    Name, Brief Bio Section
Recipe Model:
    Title, author, Description, Time Req, Instructions

"""


from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField()

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    time_req = models.CharField(max_length=50)
    instructions = models.TextField()
    post_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} - {self.author.name}'
