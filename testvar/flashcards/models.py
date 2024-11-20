from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)

class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])

class FlashcardSet(models.Model):
    name = models.CharField(max_length=200)
    cards = models.ManyToManyField(Flashcard, related_name="flashcard_sets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Collection(models.Model):
    name = models.CharField(max_length=200)
    sets = models.ManyToManyField(FlashcardSet, related_name="collections")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
