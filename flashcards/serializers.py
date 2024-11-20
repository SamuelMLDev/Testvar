from rest_framework import serializers
from .models import User, Flashcard, FlashcardSet, Collection

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_admin']

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'question', 'answer', 'difficulty', 'hidden']

class FlashcardSetSerializer(serializers.ModelSerializer):
    cards = FlashcardSerializer(many=True)

    class Meta:
        model = FlashcardSet
        fields = ['id', 'name', 'cards', 'created_at', 'updated_at', 'rating']

class CollectionSerializer(serializers.ModelSerializer):
    sets = FlashcardSetSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'sets', 'user']
