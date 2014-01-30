from django.db import models
from django.utils import timezone

class Card(models.Model):
	cardType = models.CharField(max_length = 1)
	text = models.CharField(max_length = 200)
	numberOfAnswers = models.IntegerField()
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
		#TODO: I get an error if these have not been saved to the database yet...should this be happening?
		self.datetimeLastPlayerJoined = timezone.now()
		self.save()
		player.save()
		self.gameplayer_set.create(game = self, player = player)

	def startGame(self):
		self.save()
		for card in Card.objects.all():
			self.gamecard_set.create(game = self, card = card)
		#TODO: assign 10 cards to each player
		self.active = 1
		self.save()

	def dealAnswerCards(self):
		for gamePlayer in self.gameplayer_set.filter(game = self):
			while len(self.gamecard_set.filter(game = self, gamePlayer = gamePlayer)) < 10:
				gameCard = self.getRandomUnassignedAnswerCard()
				gameCard.gamePlayer = gamePlayer
				gameCard.save()

	def getRandomUnassignedAnswerCard(self):
		return self.gamecard_set.filter(game = self, card__cardType = "A", gamePlayer_id = None).order_by("?").first()

	def newRound(self):
		self.save()
		self.gameround_set.create(
			game = self,
			question = self.getGameRoundQuestion(),
			gamePlayerQuestioner = self.getNextGameRoundGamePlayerQuestioner()
		)

	def getRandomUnusedQuestionQuestionCard(self):
		return self.gamecard_set.filter(game = self, card__cardType = "Q")

class GamePlayer(models.Model):
	game = models.ForeignKey(Game)
	player = models.ForeignKey(Player)

class GameCard(models.Model):
	game = models.ForeignKey(Game)
	card = models.ForeignKey(Card)
	gamePlayer = models.ForeignKey(GamePlayer, null = True)

class GameRound(models.Model):
	game = models.ForeignKey(Game)
	question = models.ForeignKey(GameCard)
	gamePlayerQuestioner = models.ForeignKey(GamePlayer)

class GameRoundAnswer(models.Model):
	gameRound = models.ForeignKey(GameRound)
	gameCard = models.ForeignKey(GameCard)
