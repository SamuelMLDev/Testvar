from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FlashcardViewSet, FlashcardSetViewSet, CollectionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'flashcards', FlashcardViewSet)
router.register(r'flashcardsets', FlashcardSetViewSet)
router.register(r'collections', CollectionViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('sets/<int:set_id>/', views.flashcard_set_detail, name='flashcard_set_detail'),
]
