from django.test import TestCase
from django.utils import timezone

from game.models import Card, Player, Game, GamePlayer, GameCard, GameRound

def createCards():
	for i in range(30):
		Card.objects.create(cardType = "A", numberOfAnswers = 0)
		Card.objects.create(cardType = "Q", numberOfAnswers = 1)

class GameMethodTests(TestCase):

	def test_addPlayer_newPlayerIsAdded(self):
		game = Game.objects.create(active = 0)
		player = Player.objects.create()
		game.addPlayer(player)
		self.assertEqual(game.gameplayer_set.all().count(), 1)
	
	def test_addPlayer_existingPlayerIsNotAdded(self):
		game = Game.objects.create(active = 0)
		player = Player.objects.create()
		game.addPlayer(player)
		game.addPlayer(player)
		self.assertEqual(game.gameplayer_set.all().count(), 1)

	def test_addPlayer_NoneIsAdded(self):
		game = Game.objects.create(active = 0)
		game.addPlayer(None)
		self.assertEqual(game.gameplayer_set.all().count(), 1)

	def test_startGame(self):
		createCards()
		game = Game.objects.create(active = 0)

		for i in range(3):
			game.addPlayer(None)

		game.startGame()

		self.assertEqual(game.active, 1)

	def test_getRandomUnusedQuestionCard_returnsRandomCard(self):
		game = Game.objects.create()
		player = Player.objects.create()
		gamePlayer = GamePlayer.objects.create(game = game, player = player)
		card1 = Card.objects.create(cardType = "Q")
		card2 = Card.objects.create(cardType = "Q")
		game.gamecard_set.create(game = game, card = card1, gamePlayer = gamePlayer)
		game.gamecard_set.create(game = game, card = card2)

		randomCard = game.getRandomUnusedQuestionCard()

		self.assertEqual(randomCard.id, card2.id)

	def test_getRandomUnusedQuestionCard_doesNotReturnAssignedCards(self):
		game = Game.objects.create()
		player = Player.objects.create()
		gamePlayer = GamePlayer.objects.create(game = game, player = player)
		card1 = Card.objects.create(cardType = "Q")
		card2 = Card.objects.create(cardType = "Q")
		game.gamecard_set.create(game = game, card = card1, gamePlayer = gamePlayer)
		game.gamecard_set.create(game = game, card = card2)

		randomCard = game.getRandomUnusedQuestionCard()

		self.assertEqual(randomCard.id, card2.id)

	def test_dealAnswerCards_eachPlayerEndsUpWith10Cards(self):
		createCards()
		game = Game.objects.create(active = 1)
		gameplayer1 = game.gameplayer_set.create(game = game)
		gameplayer2 = game.gameplayer_set.create(game = game)

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

	def test_isReadyToStartNewRound_returnsTrueIfActiveAndThereIsNoPriorRound(self):
		game = Game.objects.create(active = 1)
		self.assertEqual(game.isReadyToStartNewRound(), True)

	def test_isReadyToStartNewRound_returnsFalseIfInactive(self):
		game = Game.objects.create(active = 0)
		self.assertEqual(game.isReadyToStartNewRound(), False)

	def test_isReadyToStartNewRound_returnsTrueIfActiveAndPriorRoundIsComplete(self):
		#TODO: there's got to be a way to mock some of this stuff
		game = Game.objects.create(active = 0)
		gameCard = game.gamecard_set.create(game = game, card = Card.objects.create())
		gamePlayer = game.gameplayer_set.create(game = game)
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = gamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 1)
		self.assertEqual(game.isReadyToStartNewRound(), False)

	def test_isReadyToStartNewRound_returnsFalseIfActiveAndPriorRoundIsNotComplete(self):
		game = Game.objects.create(active = 0)
		gameCard = game.gamecard_set.create(game = game, card = Card.objects.create())
		gamePlayer = game.gameplayer_set.create(game = game)
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = gamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 0)
		self.assertEqual(game.isReadyToStartNewRound(), False)

	def test_gamePlayerSubmitsAnswerCard_returnsFalseIfThereIsNoCurrentRound(self):
		game = Game.objects.create(active = 0)
		gamePlayer = game.gameplayer_set.create(game = game)
		gameCard = game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())
		self.assertEqual(game.gamePlayerSubmitsAnswerCard(gamePlayer, gameCard), False)

	def test_gamePlayerSubmitsAnswerCard_returnsFalseIfCurrentRoundIsComplete(self):
		game = Game.objects.create(active = 0)
		gamePlayer = game.gameplayer_set.create(game = game)
		gameCard = game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())
		otherGamePlayer = game.gameplayer_set.create(game = game)
		otherGameCard = game.gamecard_set.create(game = game, gamePlayer = otherGamePlayer, card = Card.objects.create())
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = otherGameCard, gamePlayerQuestioner = otherGamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 1)
		self.assertEqual(game.gamePlayerSubmitsAnswerCard(gamePlayer, gameCard), False)

	def test_gamePlayerSubmitsAnswerCard_returnsFalseIfGamePlayerAlreadyAnsweredThisRound(self):
		game = Game.objects.create(active = 0)
		gamePlayer = game.gameplayer_set.create(game = game)
		gameCard = game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())
		otherGamePlayer = game.gameplayer_set.create(game = game)
		otherGameCard = game.gamecard_set.create(game = game, gamePlayer = otherGamePlayer, card = Card.objects.create())
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = otherGameCard, gamePlayerQuestioner = otherGamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 0)
		self.assertEqual(game.gamePlayerSubmitsAnswerCard(gamePlayer, gameCard), False)

	def test_gamePlayerSubmitsAnswerCard_returnsFalseIfGamePlayerIsGamePlayerQuestioner(self):
		game = Game.objects.create(active = 0)
		gamePlayer = game.gameplayer_set.create(game = game)
		gameCard = game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())
		otherGamePlayer = game.gameplayer_set.create(game = game)
		otherGameCard = game.gamecard_set.create(game = game, gamePlayer = otherGamePlayer, card = Card.objects.create())
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = otherGameCard, gamePlayerQuestioner = gamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 0)
		self.assertEqual(game.gamePlayerSubmitsAnswerCard(gamePlayer, gameCard), False)

	def test_gamePlayerSubmitsAnswerCard_returnsTrueAndOtherAssertionsWhenEverythingIsSetJustRight(self):
		game = Game.objects.create(active = 0)
		gamePlayer = game.gameplayer_set.create(game = game)
		gameCard = game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())
		otherGamePlayer = game.gameplayer_set.create(game = game)
		otherGameCard = game.gamecard_set.create(game = game, gamePlayer = otherGamePlayer, card = Card.objects.create())
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = otherGameCard, gamePlayerQuestioner = otherGamePlayer)

		self.assertEqual(game.gamePlayerSubmitsAnswerCard(gamePlayer, gameCard), True)
		self.assertEqual(gameCard.gamePlayer, None)
		self.assertEqual(gameRound.gameroundanswer_set.all().count(), 1)

	def test_gamePlayerPicksWinningAnswerCard_winnerIsSet(self):
		game = Game.objects.create(active = 0)
		gamePlayer = game.gameplayer_set.create(game = game)
		gameCard = game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = gamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 0)

		game.gamePlayerPicksWinningAnswerCard(gamePlayer, gameCard)
		self.assertEqual(gameRound.gameroundanswer_set.all().first().winner, 1)

	def test_gamePlayerPicksWinningAnswerCard_returnsFalseIfRoundIsComplete(self):
		game = Game.objects.create(active = 0)
		gamePlayer = game.gameplayer_set.create(game = game)
		gameCard = game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = gamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 1)

		self.assertEqual(game.gamePlayerPicksWinningAnswerCard(gamePlayer, gameCard), False)

	def test_gamePlayerPicksWinningAnswerCard_returnsFalseIfGamePlayerIsNotTheRoundQuestioner(self):
		game = Game.objects.create(active = 0)
		gamePlayer = game.gameplayer_set.create(game = game)
		otherGamePlayer = game.gameplayer_set.create(game = game)
		gameCard = game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = otherGamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 0)

		self.assertEqual(game.gamePlayerPicksWinningAnswerCard(gamePlayer, gameCard), False)

class GameRoundMethodTests(TestCase):

	def test_isComplete_returnsTrueWhenThereIsAWinner(self):
		game = Game.objects.create()
		gameCard = game.gamecard_set.create(game = game, card = Card.objects.create())
		gamePlayer = game.gameplayer_set.create(game = game)
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = gamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 1)
		self.assertEqual(gameRound.isComplete(), True)

	def test_isComplete_returnsFalseWhenThereIsNotAWinner(self):
		game = Game.objects.create()
		gameCard = game.gamecard_set.create(game = game, card = Card.objects.create())
		gamePlayer = game.gameplayer_set.create(game = game)
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = gamePlayer)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer, winner = 0)
		self.assertEqual(gameRound.isComplete(), False)

	def test_allAnswersHaveBeenSubmitted_returnTrue(self):
		game = Game.objects.create()
		gameCard = game.gamecard_set.create(game = game, card = Card.objects.create())
		gamePlayer1 = game.gameplayer_set.create(game = game)
		gamePlayer2 = game.gameplayer_set.create(game = game)
		gamePlayer3 = game.gameplayer_set.create(game = game)
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = gamePlayer1)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer2, winner = 0)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer3, winner = 0)
		self.assertEqual(gameRound.allAnswersHaveBeenSubmitted(), True)

	def test_allAnswersHaveBeenSubmitted_returnFalseIfAPlayerHasNotAnswered(self):
		game = Game.objects.create()
		gameCard = game.gamecard_set.create(game = game, card = Card.objects.create())
		gamePlayer1 = game.gameplayer_set.create(game = game)
		gamePlayer2 = game.gameplayer_set.create(game = game)
		gamePlayer3 = game.gameplayer_set.create(game = game)
		gameRound = game.gameround_set.create(game = game, gameCardQuestion = gameCard, gamePlayerQuestioner = gamePlayer1)
		gameRoundAnswer = gameRound.gameroundanswer_set.create(gameRound = gameRound, gameCard = gameCard, gamePlayer = gamePlayer2, winner = 0)
		self.assertEqual(gameRound.allAnswersHaveBeenSubmitted(), False)

class GamePlayerMethodTests(TestCase):

	def test_getRandomAnswerCard_returnsRandomCard(self):
		game = Game.objects.create()
		gamePlayer = game.gameplayer_set.create()

		for i in range(100):
			game.gamecard_set.create(game = game, gamePlayer = gamePlayer, card = Card.objects.create())

		cards = []
		for i in range(10):
			randomCard = gamePlayer.getRandomAnswerCard()
			if randomCard != None and randomCard not in cards:
				cards.append(randomCard)

		self.assertEqual(len(cards) > 5, True)
