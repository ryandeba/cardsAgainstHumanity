$(function(){

	cardsAgainstHumanity.Game = Backbone.Model.extend({
		defaults: {
			active: undefined,
			gamePlayers: [],
			gameRounds: [],
			thisPlayersAnswerCards: []
		},

		initialize: function(){
			var self = this;
			self.load();
			self.listenTo(self, "addBot", self.addBot);
			self.listenTo(self, "start", self.start);
			self.listenTo(self, "submitAnswer", self.submitAnswer);
			self.listenTo(self, "chooseWinner", self.chooseWinner);

			setInterval(function(){
				self.load();
			}, 5000);
		},

		toJSON: function(){
			return _.extend(this.attributes, {
				currentRoundQuestioner: this.getCurrentRoundQuestioner(),
				currentRoundQuestion: this.getCurrentRoundQuestion(),
				currentRoundAnswers: this.getCurrentRoundAnswers(),
				currentRoundWinner: this.getCurrentRoundWinner(),
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

		getCurrentRoundAnswers: function(){
			if (this.get("gameRounds").length == 0)
				return [];
			return _.last(this.get("gameRounds")).answers
		},

		getCurrentRoundWinner: function(){
			if (this.get("gameRounds").length == 0)
				return undefined;
			var lastRound = _.last(this.get("gameRounds"));
			var winningAnswer = _.findWhere(lastRound.answers, {winner: 1});
			if (winningAnswer == undefined)
				return undefined
			return _.findWhere(this.get("gamePlayers"), {id: winningAnswer.gameplayer_id});
		},

		getThisPlayersAnswerCards: function(){
			return this.get("thisPlayersAnswerCards");
			var thisGamePlayer = _.findWhere(this.get("gamePlayers"), {hash: cardsAgainstHumanity.playerhash});
			return thisGamePlayer != undefined ? thisGamePlayer.gameCards : [];
		},

		getCompletedGameRoundIDList: function(){
			var result = "";
			_.each( _.where(this.get("gameRounds"), {isComplete: true}), function(gameRound){
				result += gameRound.id + ",";
			});
			return result;
		},

		getThisPlayerAnswerCardsIDList: function(){
			var result = "";
			_.each(this.get("thisPlayersAnswerCards"), function(answerCard){
				result += answerCard.card_id + ",";
			});
			return result;
		},

		load: function(){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id") + "?gr_id=" + self.getCompletedGameRoundIDList() + "&tpac_id=" + self.getThisPlayerAnswerCardsIDList(),
				success: function(response){
					self.loadSuccess(response);
				}
			});
		},

		loadSuccess: function(response){
			response.thisPlayersAnswerCards = this.get("thisPlayersAnswerCards").concat(response.thisPlayersAnswerCards);
			response.gameRounds = this.get("gameRounds").concat(response.gameRounds);
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
			self.set("thisPlayersAnswerCards", _.without(self.get("thisPlayersAnswerCards"),
				_.findWhere(self.get("thisPlayersAnswerCards"), {card_id: parseInt(data.id)})
			));
			$.ajax({
				url: "/game/" + self.get("id") + "/submitAnswer/" + data.id,
				success: function(response){ self.load(); }
			});
		},

		chooseWinner: function(data){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id") + "/chooseWinner/" + data.id,
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
			"click .js-round-answer": "chooseWinner"
		},

		addBot: function(){ this.model.trigger("addBot"); },

		startGame: function(){ this.model.trigger("start"); },

		submitAnswer: function(e){
			//I really hate that I'm doing this
			this.model.trigger("submitAnswer", {id: $(e.currentTarget).attr("data-id") });
		},

		chooseWinner: function(e){
			this.model.trigger("chooseWinner", {id: $(e.currentTarget).attr("data-id") });
		}
	});

	var GameRound = Backbone.Model.extend({
	});

	var GameRounds = Backbone.Collection.extend({
		model: GameRound
	});

});
