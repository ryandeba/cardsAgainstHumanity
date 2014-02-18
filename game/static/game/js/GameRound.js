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
		},

		updateAnswerCards: function(){
			this.get("answerCards").set(this.get("answers"), {remove: false});
		}
	});

	cardsAgainstHumanity.CurrentRoundView = Backbone.Marionette.Layout.extend({
		template: "#template-currentround",

		regions: {
			answerCardsRegion: "#currentround-answercards"
		},

		onRender: function(){
			var self = this;
			if (_.isUndefined(self.answerCardsRegion.currentView)){
				self.answerCardsRegion.show(new cardsAgainstHumanity.GameRoundAnswerCardsView({ collection: self.model.get("answerCards") }));
			}
		}
	});

	cardsAgainstHumanity.GameRounds = Backbone.Collection.extend({
		model: cardsAgainstHumanity.GameRound
	});

	cardsAgainstHumanity.GameRoundAnwerCardView = Backbone.Marionette.ItemView.extend({
		template: "#template-answercard",

		events: {
			"click": "onClick"
		},

		attributes: {
			"class": "col-md-3 col-sm-4 col-xs-6"
		},

		onClick: function(){
			cardsAgainstHumanity.vent.trigger("game:chooseWinner", this.model);
		}
	});

	cardsAgainstHumanity.GameRoundAnswerCardsView = Backbone.Marionette.CollectionView.extend({
		itemView: cardsAgainstHumanity.GameRoundAnwerCardView
	});

});
