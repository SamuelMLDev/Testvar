from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

class Flashcard(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]
    
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    hidden = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.question

class FlashcardSet(models.Model):
    name = models.CharField(max_length=200)
    cards = models.ManyToManyField(Flashcard, related_name="flashcard_sets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0)
    total_rating = models.FloatField(default=0.0)
    number_of_ratings = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_sets', null=True, blank=True)  # Made nullable temporarily

    def update_rating(self, new_rating: float) -> None:
        self.total_rating += new_rating
        self.number_of_ratings += 1
        self.rating = self.total_rating / self.number_of_ratings
        self.save()

    def __str__(self) -> str:
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=200)
    sets = models.ManyToManyField(FlashcardSet, related_name="collections")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.name} by {self.user.username}"

class SetLimit(models.Model):
    limit = models.IntegerField(default=20)

    def __str__(self) -> str:
        return f"Daily Set Limit: {self.limit}"

class HiddenCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    hidden_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'card')

    def __str__(self) -> str:
        return f"{self.user.username} hid {self.card.id}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    completion_time = models.DurationField()
    
    def __str__(self) -> str:
        return f"{self.user.username} attempted {self.flashcard_set.name} at {self.attempt_time}"
