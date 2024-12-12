# flashcards/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .models import (
    User, FlashcardSet, Flashcard, Collection, SetLimit, HiddenCard, QuizAttempt
)
from .serializers import (
    UserSerializer, FlashcardSerializer, FlashcardSetSerializer,
    CollectionSerializer, QuizAttemptSerializer
)
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm  # Imported CustomUserCreationForm

@login_required
def home(request):
    sets = FlashcardSet.objects.all()
    return render(request, 'flashcards/home.html', {'sets': sets})

@login_required
def flashcard_set_detail(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    return render(request, 'flashcards/set_detail.html', {'flashcard_set': flashcard_set})

@login_required
def hide_card(request, card_id):
    if request.method == 'POST':
        card = get_object_or_404(Flashcard, id=card_id)
        HiddenCard.objects.get_or_create(user=request.user, card=card)
        return HttpResponseRedirect(reverse('flashcard_set_detail', args=[card.flashcard_sets.first().id]))
    return HttpResponseForbidden()

@login_required
def rate_set(request, set_id):
    if request.method == 'POST':
        flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
        try:
            rating = float(request.POST['rating'])
            if 1 <= rating <= 5:
                flashcard_set.update_rating(rating)
                return HttpResponseRedirect(reverse('flashcard_set_detail', args=[set_id]))
            else:
                # Handle invalid rating
                return HttpResponseForbidden("Invalid rating value.")
        except (ValueError, KeyError):
            # Handle missing or invalid rating
            return HttpResponseForbidden("Invalid rating value.")
    return HttpResponseForbidden()

# Authentication Views

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'flashcards/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'flashcards/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return HttpResponseForbidden()

# DRF ViewSets for API Endpoints

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Only accessible by admin users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class FlashcardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows flashcards to be viewed or edited.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def hide(self, request, pk=None):
        flashcard = self.get_object()
        HiddenCard.objects.get_or_create(user=request.user, card=flashcard)
        return Response({'status': 'flashcard hidden'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unhide(self, request, pk=None):
        flashcard = self.get_object()
        HiddenCard.objects.filter(user=request.user, card=flashcard).delete()
        return Response({'status': 'flashcard unhidden'}, status=status.HTTP_200_OK)

class FlashcardSetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows flashcard sets to be viewed or edited.
    """
    queryset = FlashcardSet.objects.all()  # Added queryset attribute
    serializer_class = FlashcardSetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FlashcardSet.objects.all()
        if self.request.user.is_authenticated:
            hidden_cards = HiddenCard.objects.filter(user=self.request.user).values_list('card_id', flat=True)
            queryset = queryset.exclude(cards__id__in=hidden_cards)
        return queryset.distinct()

    def perform_create(self, serializer):
        user = self.request.user
        today = timezone.now().date()
        sets_created_today = FlashcardSet.objects.filter(created_at__date=today, user=user).count()
        set_limit = SetLimit.objects.first().limit
        if sets_created_today >= set_limit and not user.is_admin:
            raise serializers.ValidationError("You have reached the maximum number of flashcard sets allowed today.")
        serializer.save(user=user)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        flashcard_set = self.get_object()
        rating = request.data.get('rating')
        if rating and 1 <= int(rating) <= 5:
            flashcard_set.update_rating(float(rating))
            return Response({'status': 'rating set'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid rating value'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def attempt_quiz(self, request, pk=None):
        flashcard_set = self.get_object()
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        try:
            start_dt = timezone.datetime.fromisoformat(start_time)
            end_dt = timezone.datetime.fromisoformat(end_time)
            completion_time = end_dt - start_dt
            QuizAttempt.objects.create(user=request.user, flashcard_set=flashcard_set, completion_time=completion_time)
            return Response({'status': 'quiz attempt recorded'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid time format'}, status=status.HTTP_400_BAD_REQUEST)

class CollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows collections to be viewed or edited.
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
