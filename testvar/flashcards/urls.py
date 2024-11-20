from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FlashcardViewSet, FlashcardSetViewSet, CollectionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'flashcards', FlashcardViewSet)
router.register(r'flashcardsets', FlashcardSetViewSet)
router.register(r'collections', CollectionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
