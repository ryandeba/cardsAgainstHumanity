$(function(){

	cardsAgainstHumanity.AnswerCard = Backbone.Model.extend({
	});

	cardsAgainstHumanity.AnswerCardView = Backbone.Marionette.ItemView.extend({
	});

	cardsAgainstHumanity.AnswerCards = Backbone.Collection.extend({
		model: cardsAgainstHumanity.AnswerCard
	});

	cardsAgainstHumanity.AnswerCardsView = Backbone.Marionette.CollectionView.extend({
	});

});
