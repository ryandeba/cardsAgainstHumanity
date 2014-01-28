from django.db import models

class Card(models.Model):
	cardType = models.CharField(max_length = 1)
	text = models.CharField(max_length = 200)
	numberOfAnswers = models.IntegerField()
	expansion = models.CharField(max_length = 100)

	def __unicode__(self):
		return self.cardType + " | " + self.text

class Game(models.Model):
	active = models.IntegerField(default = 1)
