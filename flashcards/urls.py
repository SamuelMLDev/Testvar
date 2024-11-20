from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sets/<int:set_id>/', views.flashcard_set_detail, name='flashcard_set_detail'),
    path('cards/<int:card_id>/hide/', views.hide_card, name='hide_card'),
    path('sets/<int:set_id>/rate/', views.rate_set, name='rate_set'),
]
