from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Flashcard, FlashcardSet, Collection
from .serializers import UserSerializer, FlashcardSerializer, FlashcardSetSerializer, CollectionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

class FlashcardSetViewSet(viewsets.ModelViewSet):
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


# Create your views here.
