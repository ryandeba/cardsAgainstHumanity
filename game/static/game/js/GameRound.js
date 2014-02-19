$(function(){

	cardsAgainstHumanity.GameRound = Backbone.Model.extend({
		defaults: {
			answers: [],
			allAnswersHaveBeenSubmitted: false,
			gamePlayerQuestionerName: ""
		},

		initialize: function(){
			var self = this;
			self.set("answerCards", new cardsAgainstHumanity.AnswerCards());
			self.updateAnswerCards();
			self.listenTo(self, "change:answers", self.updateAnswerCards);
			self.listenTo(self, "change:isComplete", self.updateAnswerCardsWithSubmitterName);
		},

		updateAnswerCards: function(){
			var self = this;
			self.get("answerCards").set(self.get("answers"), {remove: false});
			self.get("answerCards").each(function(answerCard){
				answerCard.set("faceUp", self.get("allAnswersHaveBeenSubmitted"));
			});
		},

		updateAnswerCardsWithSubmitterName: function(){
			if (this.get("isComplete")){
				cardsAgainstHumanity.vent.trigger("game:updateSubmittedBy", this.get("answerCards"));
			}
		},

		getWinnerGamePlayerID: function(){
			var self = this;
			var winningAnswerCard = self.get("answerCards").findWhere({winner: true});
			return winningAnswerCard == undefined ? undefined : winningAnswerCard.get("gameplayer_id");
		}
	});

	cardsAgainstHumanity.CurrentRoundView = Backbone.Marionette.Layout.extend({
		template: "#template-currentround",

		regions: {
			answerCardsRegion: "#currentround-answercards"
		},

		initialize: function(){
			this.listenTo(this.model, "change:gamePlayerQuestionerName", this.render);
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
		template: "#template-gameroundanswercard",

		events: {
			"click": "onClick"
		},

		attributes: {
			"class": "col-md-3 col-sm-4 col-xs-6"
		},

		initialize: function(){
			this.listenTo(this.model, "change", this.render);
		},

		onClick: function(){
			cardsAgainstHumanity.vent.trigger("game:chooseWinner", this.model);
		}
	});

	cardsAgainstHumanity.GameRoundAnswerCardsView = Backbone.Marionette.CollectionView.extend({
		itemView: cardsAgainstHumanity.GameRoundAnwerCardView
	});

});
