from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Flashcard, FlashcardSet

def home(request):
    sets = FlashcardSet.objects.all()
    return render(request, 'flashcards/home.html', {'sets': sets})

def flashcard_set_detail(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    return render(request, 'flashcards/set_detail.html', {'flashcard_set': flashcard_set})

def hide_card(request, card_id):
    if request.method == 'POST':
        card = get_object_or_404(Flashcard, id=card_id)
        card.hidden = True
        card.save()
        return HttpResponseRedirect(reverse('flashcard_set_detail', args=[card.flashcard_sets.first().id]))

def rate_set(request, set_id):
    if request.method == 'POST':
        flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
        rating = float(request.POST['rating'])
        flashcard_set.rating = (flashcard_set.rating + rating) / 2  # Simplified logic
        flashcard_set.save()
        return HttpResponseRedirect(reverse('flashcard_set_detail', args=[set_id]))
