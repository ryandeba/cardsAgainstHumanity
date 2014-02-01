from django.db import models
from django.utils import timezone

class Card(models.Model):
	cardType = models.CharField(max_length = 1)
	text = models.CharField(max_length = 200)
	numberOfAnswers = models.IntegerField(default = 1)
	expansion = models.CharField(max_length = 100)

	def __unicode__(self):
		return self.cardType + " | " + self.text

class Player(models.Model):
	hash = models.CharField(max_length = 32)
	name = models.CharField(max_length = 50)

class Game(models.Model):
	active = models.IntegerField(default = 0) #0 - lobby, 1 - active
	datetimeLastPlayerJoined = models.DateTimeField(auto_now = True)

	def addPlayer(self, player):
		if self.active != 0:
			return False
		self.datetimeLastPlayerJoined = timezone.now()
		self.gameplayer_set.create(game = self, player = player)

	def startGame(self):
		for card in Card.objects.exclude(numberOfAnswers = 2):
			self.gamecard_set.create(game = self, card = card)

		self.dealAnswerCards()
		self.active = 1
		#self.newRound()
		self.save()

	def dealAnswerCards(self):
		for gamePlayer in self.gameplayer_set.filter(game = self):
			while len(self.gamecard_set.filter(game = self, gamePlayer = gamePlayer)) < 10:
				gameCard = self.getRandomUnassignedAnswerCard()
				gameCard.gamePlayer = gamePlayer
				gameCard.save()

	def getRandomUnassignedAnswerCard(self):
		return self.gamecard_set.filter(game = self, card__cardType = "A", gamePlayer_id = None).order_by("?").first()

	def getRandomUnusedQuestionQuestionCard(self):
		return self.gamecard_set.filter(game = self, card__cardType = "Q", gamePlayer_id = None).order_by("?").first()

	def newRound(self):
		self.gameround_set.create(
			game = self,
			question = self.getRandomUnusedQuestionQuestionCard(),
			gamePlayerQuestioner = self.getNextGameRoundGamePlayerQuestioner()
		)

	def getNextGameRoundGamePlayerQuestioner(self):
		if self.gameround_set.filter(game = self).count() > 0:
			lastGameRound = self.gameround_set.filter(game = self).order_by("id").first()
			lastGamePlayerQuestioner = lastGameRound.gamePlayerQuestioner

			gamePlayers = self.gameplayer_set.filter(game = self).order_by("id")
			foundTheLastPlayer = False
			for gamePlayer in gamePlayers:
				if foundTheLastPlayer:
					return gamePlayer
				if gamePlayer.id == lastGamePlayerQuestioner.id:
					foundTheLastPlayer = True
			return gamePlayers[0]
		else:
			return self.gameplayer_set.filter(game = self).order_by("?").first()

class GamePlayer(models.Model):
	game = models.ForeignKey(Game)
	player = models.ForeignKey(Player, null = True)

class GameCard(models.Model):
	game = models.ForeignKey(Game)
	card = models.ForeignKey(Card)
	gamePlayer = models.ForeignKey(GamePlayer, null = True)

class GameRound(models.Model):
	game = models.ForeignKey(Game)
	gameCardQuestion = models.ForeignKey(GameCard)
	gamePlayerQuestioner = models.ForeignKey(GamePlayer)

class GameRoundAnswer(models.Model):
	gameRound = models.ForeignKey(GameRound)
	gameCard = models.ForeignKey(GameCard)
