from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Flashcard, FlashcardSet, Collection, SetLimit
from django.utils import timezone
from datetime import timedelta

class FlashcardSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_admin=True)
        self.normal_user = User.objects.create_user(username='user', password='userpass')
        self.set_limit = SetLimit.objects.create(limit=20)
        self.client.login(username='user', password='userpass')

    def test_create_flashcard_set_under_limit(self):
        url = reverse('flashcardset-list')
        data = {
            'name': 'Test Set',
            'cards': [],
            'user': self.normal_user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_flashcard_set_over_limit(self):
        # Create 20 sets
        for _ in range(20):
            FlashcardSet.objects.create(name='Set', user=self.normal_user)
        url = reverse('flashcardset-list')
        data = {
            'name': 'Exceed Set',
            'cards': [],
            'user': self.normal_user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_rate_flashcard_set_valid(self):
        flashcard_set = FlashcardSet.objects.create(name='Rate Set', user=self.normal_user)
        url = reverse('flashcardset-rate', kwargs={'pk': flashcard_set.id})
        data = {'rating': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        flashcard_set.refresh_from_db()
        self.assertEqual(flashcard_set.rating, 2.5)  # (0 + 5) / 2

    def test_rate_flashcard_set_invalid(self):
        flashcard_set = FlashcardSet.objects.create(name='Rate Set', user=self.normal_user)
        url = reverse('flashcardset-rate', kwargs={'pk': flashcard_set.id})
        data = {'rating': 6}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class FlashcardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='userpass')
        self.client.login(username='user', password='userpass')
        self.flashcard = Flashcard.objects.create(question='Q1', answer='A1', difficulty='easy')

    def test_hide_flashcard(self):
        url = reverse('flashcard-hide', kwargs={'pk': self.flashcard.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flashcard.refresh_from_db()
        self.assertTrue(self.flashcard.hidden)

class CollectionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='userpass')
        self.client.login(username='user', password='userpass')
        self.flashcard_set = FlashcardSet.objects.create(name='Set1', user=self.user)
        self.collection = Collection.objects.create(name='Collection1', user=self.user)
        self.collection.sets.add(self.flashcard_set)

    def test_create_collection(self):
        url = reverse('collection-list')
        data = {'name': 'New Collection', 'sets': [self.flashcard_set.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_collection(self):
        url = reverse('collection-detail', kwargs={'pk': self.collection.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
