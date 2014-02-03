$(function(){

	cardsAgainstHumanity.Game = Backbone.Model.extend({
		defaults: {
			active: 0,
			gamePlayers: [],
			gameRounds: []
		},

		initialize: function(){
			this.load();
			this.listenTo(this, "addBot", this.addBot);
			this.listenTo(this, "start", this.start);
			this.listenTo(this, "submitAnswer", this.submitAnswer);
			this.listenTo(this, "forceAnswers", this.forceAnswers);
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
			var currentRoundQuestioner_id = _.last(this.get("gameRounds")).gamePlayerQuestioner_id;
			return _.findWhere(this.get("gamePlayers"), {id: currentRoundQuestioner_id});
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
		},

		addBot: function(){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id") + "/addBot",
				success: function(response){ self.load(); }
			});
		},

		start: function(){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id") + "/startGame",
				success: function(response){ self.load(); }
			});
		},

		submitAnswer: function(data){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id") + "/submitAnswer/" + data.id,
				success: function(response){ self.load(); }
			});
		},

		forceAnswers: function(){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id") + "/forceAnswers",
				success: function(response){ self.load(); }
			});
		}
	});

	cardsAgainstHumanity.GameView = Backbone.Marionette.ItemView.extend({
		template: "#template-game",

		initialize: function(){
			this.listenTo(this.model, "change", this.render);
		},

		events: {
			"click .js-add-bot": "addBot",
			"click .js-startgame": "startGame",
			"click .js-answercard": "submitAnswer",
			"click .js-forceanswers": "forceAnswers",
		},

		addBot: function(){
			this.model.trigger("addBot");
		},

		startGame: function(){
			this.model.trigger("start");
		},

		submitAnswer: function(e){
			//I really hate that I'm doing this
			this.model.trigger("submitAnswer", {id: $(e.currentTarget).attr("data-id") });
		},

		forceAnswers: function(){
			this.model.trigger("forceAnswers");
		}
	});

	var GameRound = Backbone.Model.extend({
	});

	var GameRounds = Backbone.Collection.extend({
		model: GameRound
	});

});
