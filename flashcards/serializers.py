# flashcards/serializers.py

from rest_framework import serializers
from .models import User, Flashcard, FlashcardSet, Collection, QuizAttempt, HiddenCard

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_admin']

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'question', 'answer', 'difficulty', 'hidden']

class FlashcardSetSerializer(serializers.ModelSerializer):
    cards = FlashcardSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = FlashcardSet
        fields = ['id', 'name', 'cards', 'created_at', 'updated_at', 'rating', 'user']

class CollectionSerializer(serializers.ModelSerializer):
    sets = FlashcardSetSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Collection
        fields = ['id', 'name', 'sets', 'user']

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'flashcard_set', 'attempt_time', 'completion_time']
