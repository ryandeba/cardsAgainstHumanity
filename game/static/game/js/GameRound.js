$(function(){

	cardsAgainstHumanity.GameRound = Backbone.Model.extend({
		defaults: {
			answers: []
		},

		initialize: function(){
			this.set("answerCards", new cardsAgainstHumanity.AnswerCards());
			this.updateAnswerCards();
			this.listenTo(this, "change:answers", this.updateAnswerCards);
		},

		updateAnswerCards: function(){
			this.get("answerCards").set(this.get("answers"), {remove: false});
		}
	});

	cardsAgainstHumanity.GameRounds = Backbone.Collection.extend({
		model: cardsAgainstHumanity.GameRound
	});

});
