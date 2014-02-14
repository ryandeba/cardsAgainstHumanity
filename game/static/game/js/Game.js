$(function(){

	cardsAgainstHumanity.Game = Backbone.Model.extend({
		defaults: {
			mode: "currentRound",
			active: undefined,
			gamePlayers: new cardsAgainstHumanity.GamePlayers(),
			gameRounds: new cardsAgainstHumanity.GameRounds(),
			thisPlayersAnswerCards: new cardsAgainstHumanity.AnswerCards(),
			lastUpdated: 0
		},

		initialize: function(){
			var self = this;
			self.load();

			self.listenTo(cardsAgainstHumanity.vent, "showGame:currentRound", self.setModeCurrentRound);
			self.listenTo(cardsAgainstHumanity.vent, "showGame:players", self.setModePlayers);
			self.listenTo(cardsAgainstHumanity.vent, "showGame:chat", self.setModeChat);
			self.listenTo(cardsAgainstHumanity.vent, "showGame:previousRounds", self.setModePreviousRounds);
			self.listenTo(self, "addBot", self.addBot);
			self.listenTo(self, "start", self.start);
			self.listenTo(self, "submitAnswer", self.submitAnswer);
			self.listenTo(self, "chooseWinner", self.chooseWinner);
			self.listenTo(self, "change:id", self.load);
			self.listenTo(self.get("thisPlayersAnswerCards"), "remove", function(){ self.trigger("change"); });

			setInterval(function(){
				self.load();
			}, 5000);
		},

		setModeCurrentRound: function(){ this.set("mode", "currentRound"); },
		setModePlayers: function(){ this.set("mode", "players"); },
		setModeChat: function(){ this.set("mode", "chat"); },
		setModePreviousRounds: function(){ this.set("mode", "previousRounds"); },

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
			var currentRoundQuestioner_id = this.get("gameRounds").last().get("gamePlayerQuestioner_id");
			return this.get("gamePlayers").findWhere({id: currentRoundQuestioner_id});
		},

		getCurrentRoundQuestion: function(){
			if (this.get("gameRounds").length == 0)
				return "";
			return this.get("gameRounds").last().get("question");
		},

		getCurrentRoundAnswers: function(){
			if (this.get("gameRounds").length == 0)
				return [];
			return this.get("gameRounds").last().get("answerCards");
		},

		getCurrentRoundWinner: function(){
			if (this.get("gameRounds").length == 0)
				return undefined;
			var lastRound = this.get("gameRounds").last();
			var winningAnswer = lastRound.get("answerCards").findWhere({winner: 1});
			if (winningAnswer == undefined)
				return undefined
			return this.get("gamePlayers").findWhere({id: winningAnswer.gameplayer_id});
		},

		getThisPlayersAnswerCards: function(){
			return this.get("thisPlayersAnswerCards");
		},

		load: function(){
			var self = this;
			if (self.get("id") == undefined){
				return;
			}
			$.ajax({
				url: "/game/" + self.get("id") + "?lastUpdated=" + self.get("lastUpdated"),
				success: function(response){ self.loadSuccess(response); }
			});
		},

		loadSuccess: function(response){
			this.get("thisPlayersAnswerCards").set(response.thisPlayersAnswerCards || [], {remove: false});
			this.get("gameRounds").set(response.gameRounds || [], {remove: false});
			this.get("gamePlayers").set(response.gamePlayers || [], {remove: false});
			delete response.thisPlayersAnswerCards;
			delete response.gameRounds;
			delete response.gamePlayers;
			this.set(response);
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

		onClose: function(){
			this.model.set("id", undefined);
		},

		events: {
			"click .js-addbot": "addBot",
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

});
