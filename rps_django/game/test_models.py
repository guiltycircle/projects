from django.test import TestCase
from .models import Game

class GameModelTest(TestCase):
    def test_game_creation(self):
        game = Game.objects.create()
        self.assertIsNotNone(game.code)
        self.assertEqual(game.player1_score, 0)
        self.assertEqual(game.player2_score, 0)
        self.assertEqual(game.status, 'waiting')

    def test_game_code_uniqueness(self):
        game1 = Game.objects.create()
        game2 = Game.objects.create()
        self.assertNotEqual(game1.code, game2.code)

    def test_score_update(self):
        game = Game.objects.create()
        game.player1_score += 1
        game.player2_score += 2
        game.save()
        updated_game = Game.objects.get(pk=game.pk)
        self.assertEqual(updated_game.player1_score, 1)
        self.assertEqual(updated_game.player2_score, 2) 