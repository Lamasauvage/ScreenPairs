from django.db import models

# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title


