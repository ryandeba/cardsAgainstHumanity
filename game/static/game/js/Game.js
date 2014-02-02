$(function(){

	cardsAgainstHumanity.Game = Backbone.Model.extend({
		defaults: {
			active: 0,
			gamePlayers: [],
			gameRounds: []
		},

		initialize: function(){
			this.load();
		},

		toJSON: function(){
			return _.extend(this.attributes, {
				currentRoundQuestioner: this.getCurrentRoundQuestioner(),
				currentRoundQuestion: this.getCurrentRoundQuestion(),
				thisPlayersAnswerCards: this.getThisPlayersAnswerCards()
			});
		},

		getCurrentRoundQuestioner: function(){
			if (this.get("gameRounds").length == 0)
				return "";
			var currentRoundQuestion_id = _.last(this.get("gameRounds")).gamePlayerQuestioner_id;
			return "{someone}";
		},

		getCurrentRoundQuestion: function(){
			if (this.get("gameRounds").length == 0)
				return "";
			return _.last(this.get("gameRounds")).question;
		},

		getThisPlayersAnswerCards: function(){
			var thisGamePlayer = _.findWhere(this.get("gamePlayers"), {hash: cardsAgainstHumanity.playerhash});
			return thisGamePlayer != undefined ? thisGamePlayer.gameCards : [];
		},

		load: function(){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id"),
				success: function(response){
					self.loadSuccess(response);
				}
			});
		},

		loadSuccess: function(response){
			this.set(response);
			this.trigger("change");
		}
	});

	cardsAgainstHumanity.GameView = Backbone.Marionette.ItemView.extend({
		template: "#template-game",

		initialize: function(){
			this.listenTo(this.model, "change", this.render);
		}
	});

	var GameRound = Backbone.Model.extend({
	});

	var GameRounds = Backbone.Collection.extend({
		model: GameRound
	});

});
