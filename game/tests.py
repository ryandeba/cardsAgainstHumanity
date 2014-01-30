from django.test import TestCase
from django.utils import timezone

from game.models import Card, Player, Game, GamePlayer, GameCard

class GameMethodTests(TestCase):

	def test_addPlayer(self):
		player = Player()
		game = Game()

		now = timezone.now()

		game.addPlayer(player)

		gamePlayers = game.gameplayer_set.all()
		
		self.assertEqual(len(gamePlayers), 1)
		self.assertEqual(True, game.datetimeLastPlayerJoined >= now)

	def test_startGame(self):
		game = Game()

		for i in range(10):
			Card(numberOfAnswers = 1).save()

		game.startGame()

		gameCards = game.gamecard_set.all()
		self.assertEqual(len(gameCards), 10)

	def test_getRandomUnassignedAnswerCard_returnsRandomCard(self):
		game = Game()
		game.save()

		for i in range(200):
			Card(text = str(i), numberOfAnswers = 1).save()

		for card in Card.objects.all():
			game.gamecard_set.create(game = game, card = card)

		cards = []
		for i in range(2):
			if card not in cards:
				cards.append(game.getRandomUnassignedAnswerCard())

		self.assertEqual(len(cards), 2)

	def test_getRandomUnassignedAnswerCard_doesNotReturnAssignedCards(self):
		game = Game()
		game.save()

		player = Player()
		player.save()

		gamePlayer = GamePlayer(game = game, player = player)
		gamePlayer.save()

		card1 = Card(cardType = "A", numberOfAnswers = 1)
		card1.save()
		card2 = Card(cardType = "A", numberOfAnswers = 1)
		card2.save()

		game.gamecard_set.create(game = game, card = card1, gamePlayer = gamePlayer)
		game.gamecard_set.create(game = game, card = card2)

		randomCard = game.getRandomUnassignedAnswerCard()

		self.assertEqual(randomCard.id, card2.id)
