from django.test import TestCase, Client
from django.urls import reverse
from .models import Game

class SinglePlayerViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_single_player_play_get(self):
        response = self.client.get(reverse('play'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rock Paper Scissors')

    def test_single_player_play_post(self):
        response = self.client.post(reverse('play'), {'choice': 'rock'})
        self.assertEqual(response.status_code, 302)  # Should redirect after play

class MultiplayerViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_game(self):
        response = self.client.get(reverse('create_game'))
        self.assertEqual(response.status_code, 302)
        # Should redirect to the multiplayer game page
        game = Game.objects.last()
        self.assertIsNotNone(game)
        self.assertIn(game.code, response.url)

    def test_join_game_invalid(self):
        response = self.client.post(reverse('join_game'), {'code': 'INVALID'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Game not found.')

    def test_join_game_valid(self):
        game = Game.objects.create()
        response = self.client.post(reverse('join_game'), {'code': game.code})
        self.assertEqual(response.status_code, 302)
        self.assertIn(game.code, response.url) 