# flashcards/urls.py

from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, FlashcardViewSet, FlashcardSetViewSet, CollectionViewSet,
    home, flashcard_set_detail, hide_card, rate_set,
    register_view, login_view, logout_view
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'flashcards', FlashcardViewSet)
router.register(r'sets', FlashcardSetViewSet)
router.register(r'collections', CollectionViewSet)

urlpatterns = [
    # Web Interface URLs
    path('', home, name='home'),
    path('sets/<int:set_id>/', flashcard_set_detail, name='flashcard_set_detail'),
    path('cards/<int:card_id>/hide/', hide_card, name='hide_card'),
    path('sets/<int:set_id>/rate/', rate_set, name='rate_set'),
    
    # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # API URLs
    path('api/', include(router.urls)),
]
