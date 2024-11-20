from django.shortcuts import render, get_object_or_404
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

def home(request):
    sets = FlashcardSet.objects.all()
    return render(request, 'flashcards/home.html', {'sets': sets})

def flashcard_set_detail(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    return render(request, 'flashcards/set_detail.html', {'flashcard_set': flashcard_set})


# Create your views here.
