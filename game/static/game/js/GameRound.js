$(function(){

	cardsAgainstHumanity.GameRound = Backbone.Model.extend({
		defaults: {
			answers: []
		},

		initialize: function(){
			var self = this;
			self.set("answerCards", new cardsAgainstHumanity.AnswerCards());
			self.updateAnswerCards();
			self.listenTo(self, "change:answers", self.updateAnswerCards);
			self.listenTo(self.get("answerCards"), "change", function(){ self.trigger("change"); });
		},

		updateAnswerCards: function(){
			this.get("answerCards").set(this.get("answers"), {remove: false});
		}
	});

	cardsAgainstHumanity.GameRounds = Backbone.Collection.extend({
		model: cardsAgainstHumanity.GameRound
	});

});
