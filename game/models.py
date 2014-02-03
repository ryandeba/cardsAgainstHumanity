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
		return "ID: %s | Active: %s | Players: %s" % (self.id, self.active, self.getNumberOfPlayers())

	def getNumberOfPlayers(self):
		return self.gameplayer_set.filter(game = self).count()

	def getSecondsSinceLastPlayerJoined(self):
		lastPlayerToJoin = self.gameplayer_set.filter(game = self).order_by("-id").first()
		if lastPlayerToJoin:
			return (timezone.now() - lastPlayerToJoin.datetimeCreated).total_seconds()
		else:
			return 0

	def startGame(self):
		self.gamecard_set.bulk_create([GameCard(game = self, card = card) for card in Card.objects.exclude(numberOfAnswers = 2)])

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

	def getHash(self):
		if self.player:
			return self.player.hash
		return ""

	def getName(self):
		if self.player and len(self.player.name) > 0:
			return self.player.name
		return "Anonymous"

class GameCard(models.Model):
	game = models.ForeignKey(Game)
	card = models.ForeignKey(Card)
	gamePlayer = models.ForeignKey(GamePlayer, null = True)

class GameRound(models.Model):
	game = models.ForeignKey(Game)
	gameCardQuestion = models.ForeignKey(GameCard)
	gamePlayerQuestioner = models.ForeignKey(GamePlayer)
	datetimeCreated = models.DateTimeField(auto_now = True)

class GameRoundAnswer(models.Model):
	gameRound = models.ForeignKey(GameRound)
	gameCard = models.ForeignKey(GameCard)
	gamePlayer = models.ForeignKey(GamePlayer)
	datetimeCreated = models.DateTimeField(auto_now = True)
	winner = models.IntegerField(default = 0)
