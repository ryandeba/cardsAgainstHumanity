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
	datetimeCreated = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.name

class Game(models.Model):
	active = models.IntegerField(default = 0) #0 - lobby, 1 - active
	datetimeCreated = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.id

	def getNumberOfPlayers(self):
		return self.gameplayer_set.filter(game = self).count()

	def getSecondsSinceLastPlayerJoined(self):
		lastPlayerToJoin = self.gameplayer_set.filter(game = self).order_by("-id").first()
		if lastPlayerToJoin:
			return (timezone.now() - lastPlayerToJoin.datetimeCreated).total_seconds()
		else:
			return 0

	def startGame(self):
		for card in Card.objects.exclude(numberOfAnswers = 2):
			self.gamecard_set.create(game = self, card = card)

		self.dealAnswerCards()
		self.active = 1
		self.newRound()
		self.save()

	def dealAnswerCards(self):
		for gamePlayer in self.gameplayer_set.filter(game = self):
			while len(self.gamecard_set.filter(game = self, gamePlayer = gamePlayer)) < 10:
				gameCard = self.getRandomUnassignedAnswerCard()
				gameCard.gamePlayer = gamePlayer
				gameCard.save()

	def getRandomUnassignedAnswerCard(self):
		return self.gamecard_set.filter(game = self, card__cardType = "A", gamePlayer_id = None).order_by("?").first()

	def getRandomUnusedQuestionCard(self):
		return self.gamecard_set.filter(game = self, card__cardType = "Q", gamePlayer_id = None).order_by("?").first()

	def newRound(self):
		self.gameround_set.create(
			game = self,
			gameCardQuestion = self.getRandomUnusedQuestionCard(),
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
	datetimeCreated = models.DateTimeField(auto_now = True)

class GameCard(models.Model):
	game = models.ForeignKey(Game)
	card = models.ForeignKey(Card)
	gamePlayer = models.ForeignKey(GamePlayer, null = True)

	def isHumanPlayer(self):
		return self.gamePlayer != None

class GameRound(models.Model):
	game = models.ForeignKey(Game)
	gameCardQuestion = models.ForeignKey(GameCard)
	gamePlayerQuestioner = models.ForeignKey(GamePlayer)
	datetimeCreated = models.DateTimeField(auto_now = True)

class GameRoundAnswer(models.Model):
	gameRound = models.ForeignKey(GameRound)
	gameCard = models.ForeignKey(GameCard)
	datetimeCreated = models.DateTimeField(auto_now = True)
