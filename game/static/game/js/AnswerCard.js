$(function(){

	cardsAgainstHumanity.AnswerCard = Backbone.Model.extend({
		idAttribute: "card_id"
	});

	cardsAgainstHumanity.AnswerCards = Backbone.Collection.extend({
		model: cardsAgainstHumanity.AnswerCard
	});

});
