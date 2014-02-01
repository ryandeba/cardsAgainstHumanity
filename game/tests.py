from django.test import TestCase
from django.utils import timezone

from game.models import Card, Player, Game, GamePlayer, GameCard, GameRound

class GameMethodTests(TestCase):

	def test_startGame(self):
		game = Game.objects.create()

		for i in range(10):
			Card.objects.create(numberOfAnswers = 1, cardType = "A")
			Card.objects.create(numberOfAnswers = 1, cardType = "Q")

		GamePlayer.objects.create(game = game)

		game.startGame()

		gameCards = game.gamecard_set.all()
		self.assertEqual(len(gameCards), 20)

	def test_getRandomUnassignedAnswerCard_returnsRandomCard(self):
		game = Game.objects.create()

		for i in range(100):
			Card(text = str(i), numberOfAnswers = 1, cardType = "A").save()

		for card in Card.objects.all():
			game.gamecard_set.create(game = game, card = card)

		cards = []
		for i in range(10):
			if card != None and card not in cards:
				cards.append(game.getRandomUnassignedAnswerCard())

		self.assertEqual(len(cards) > 5, True)

	def test_getRandomUnassignedAnswerCard_doesNotReturnAssignedCards(self):
		game = Game.objects.create()

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

	def test_getRandomUnusedQuestionCard_returnsRandomCard(self):
		game = Game.objects.create()

		player = Player()
		player.save()

		gamePlayer = GamePlayer(game = game, player = player)
		gamePlayer.save()

		card1 = Card(cardType = "Q", numberOfAnswers = 1)
		card1.save()
		card2 = Card(cardType = "Q", numberOfAnswers = 1)
		card2.save()

		game.gamecard_set.create(game = game, card = card1, gamePlayer = gamePlayer)
		game.gamecard_set.create(game = game, card = card2)

		randomCard = game.getRandomUnusedQuestionCard()

		self.assertEqual(randomCard.id, card2.id)

	def test_getRandomUnusedQuestionCard_doesNotReturnAssignedCards(self):
		game = Game.objects.create()
		player = Player.objects.create()

		gamePlayer = GamePlayer.objects.create(game = game, player = player)

		card1 = Card.objects.create(cardType = "Q", numberOfAnswers = 1)
		card2 = Card.objects.create(cardType = "Q", numberOfAnswers = 1)

		game.gamecard_set.create(game = game, card = card1, gamePlayer = gamePlayer)
		game.gamecard_set.create(game = game, card = card2)

		randomCard = game.getRandomUnusedQuestionCard()

		self.assertEqual(randomCard.id, card2.id)

	def test_dealAnswerCards_eachPlayerEndsUpWith10Cards(self):
		game = Game.objects.create()
		gameplayer1 = game.gameplayer_set.create(game = game)
		gameplayer2 = game.gameplayer_set.create(game = game)

		for i in range(100):
			card = Card.objects.create(numberOfAnswers = 1, cardType = "A")
			game.gamecard_set.create(game = game, card = card)

		game.dealAnswerCards()

		self.assertEqual(game.gamecard_set.filter(card__cardType = "A", gamePlayer_id = gameplayer1.id).count(), 10)
		self.assertEqual(game.gamecard_set.filter(card__cardType = "A", gamePlayer_id = gameplayer2.id).count(), 10)

	def test_getNextGameRoundGamePlayerQuestioner_playerReturnedWhenThereAreNoGameRounds(self):
		game = Game.objects.create()
		gameplayer1 = GamePlayer.objects.create(game = game)

		nextRoundGamePlayer = game.getNextGameRoundGamePlayerQuestioner()
		self.assertEqual(nextRoundGamePlayer.id, gameplayer1.id)

	def test_getNextGameRoundGamePlayerQuestioner_secondPlayerReturnedIfFirstPlayerWentLastRound(self):
		game = Game.objects.create()
		gameplayer1 = GamePlayer.objects.create(game = game)
		gameplayer2 = GamePlayer.objects.create(game = game)
		card = Card.objects.create()
		gameCard = GameCard.objects.create(game = game, card = card)
		gameround1 = GameRound.objects.create(game = game, gamePlayerQuestioner = gameplayer1, gameCardQuestion = gameCard)

		nextRoundGamePlayer = game.getNextGameRoundGamePlayerQuestioner()
		self.assertEqual(nextRoundGamePlayer.id, gameplayer2.id)

	def test_getNextGameRoundGamePlayerQuestioner_firstPlayerReturnedIfSecondPlayerWentLastRound(self):
		game = Game.objects.create()
		gameplayer1 = GamePlayer.objects.create(game = game)
		gameplayer2 = GamePlayer.objects.create(game = game)
		card = Card.objects.create()
		gameCard = GameCard.objects.create(game = game, card = card)
		gameround1 = GameRound.objects.create(game = game, gamePlayerQuestioner = gameplayer2, gameCardQuestion = gameCard)

		nextRoundGamePlayer = game.getNextGameRoundGamePlayerQuestioner()
		self.assertEqual(nextRoundGamePlayer.id, gameplayer1.id)
