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
			self.listenTo(cardsAgainstHumanity.vent, "game:submitAnswer", self.submitAnswer);
			self.listenTo(cardsAgainstHumanity.vent, "game:chooseWinner", self.chooseWinner);
			self.listenTo(cardsAgainstHumanity.vent, "game:updateSubmittedBy", self.updateSubmittedBy);
			self.listenTo(self.get("gameRounds"), "add", function(){ self.trigger("add:gameRound"); });
			self.listenTo(self, "addBot", self.addBot);
			self.listenTo(self, "start", self.start);
			self.listenTo(self, "change:id", self.load);

			setInterval(function(){
				self.load();
			}, 5000);
		},

		setModeCurrentRound: function(){ this.set("mode", "currentRound"); },
		setModePlayers: function(){ this.set("mode", "players"); },
		setModeChat: function(){ this.set("mode", "chat"); },
		setModePreviousRounds: function(){ this.set("mode", "previousRounds"); },

		updateSubmittedBy: function(answerCards){
			var self = this;
			answerCards.each(function(answerCard){
				answerCard.set(
					"submittedBy",
					self.get("gamePlayers").findWhere({id: answerCard.get("gameplayer_id")}).get("name")
				);
			});
		},

		getCurrentRound: function(){
			return this.get("gameRounds").last();
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
			this.get("gamePlayers").set(response.gamePlayers || [], {remove: false});
			this.get("gameRounds").set(response.gameRounds || [], {remove: false});
			delete response.thisPlayersAnswerCards;
			delete response.gamePlayers;
			delete response.gameRounds;
			this.updateGamePlayerNamesIntoGameRounds();
			this.updateGamePlayerScores();
			this.set(response);
		},

		updateGamePlayerNamesIntoGameRounds: function(){
			var self = this;
			self.get("gameRounds").each(function(gameRound){
				gameRound.set(
					"gamePlayerQuestionerName",
					self.get("gamePlayers").findWhere({id: gameRound.get("gamePlayerQuestioner_id")}).get("name")
				);
			});
		},

		updateGamePlayerScores: function(){
			var self = this;
			self.get("gamePlayers").each(function(gamePlayer){
				var score = 0;
				self.get("gameRounds").each(function(gameRound){
					score += gameRound.getWinnerGamePlayerID() == gamePlayer.get("id") ? 1 : 0;
				});
				gamePlayer.set("score", score);
			});
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

		submitAnswer: function(card){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id") + "/submitAnswer/" + card.get("card_id"),
				success: function(response){ 
					self.get("thisPlayersAnswerCards").remove(card);
					self.load();
				}
			});
		},

		chooseWinner: function(card){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id") + "/chooseWinner/" + card.get("card_id"),
				success: function(response){ self.load(); }
			});
		}
	});

	cardsAgainstHumanity.GameLayout = Backbone.Marionette.Layout.extend({
		template: "#template-game",

		regions: {
			navRegion: "#game-nav",
			mainRegion: "#game-main",
			answerCardsRegion: "#game-answercards"
		},

		initialize: function(){
			this.listenTo(this.model, "change:active", this.onModelChange);
			this.listenTo(this.model, "change:mode", this.onModelChange);
			this.listenTo(this.model, "add:gameRound", this.onModelChange);
		},

		onClose: function(){
			this.model.set("id", undefined);
		},

		onRender: function(){
			this.navRegion.show(new cardsAgainstHumanity.GameNavView({ model: this.model }));
			this.answerCardsRegion.show(new cardsAgainstHumanity.AnswerCardsView({ collection: this.model.get("thisPlayersAnswerCards") }));
		},

		onModelChange: function(){
			var self = this;
			var mainRegionView;
			if (self.model.get("active") == 0 && self.model.get("mode") == "currentRound"){
				mainRegionView = new cardsAgainstHumanity.PregameView({ model: self.model });
			}
			else if (self.model.get("mode") == "currentRound"){
				mainRegionView = new cardsAgainstHumanity.CurrentRoundView({ model: self.model.getCurrentRound() });
			}
			else if (self.model.get("mode") == "players"){
				mainRegionView = new cardsAgainstHumanity.GamePlayersView({ collection: self.model.get("gamePlayers") });
			}
			else if (self.model.get("mode") == "previousRounds"){
				mainRegionView = new cardsAgainstHumanity.GameRoundsView({ collection: self.model.get("gameRounds") });
			}
			if (mainRegionView != undefined){
				self.mainRegion.show(mainRegionView);
			}
		}
	});

	cardsAgainstHumanity.GameNavView = Backbone.Marionette.ItemView.extend({
		template: "#template-gamenav",

		initialize: function(){
			this.listenTo(this.model, "change", this.render);
		}
	});

	cardsAgainstHumanity.PregameView = Backbone.Marionette.ItemView.extend({
		template: "#template-pregame",

		events: {
			"click .js-addbot": "addBot",
			"click .js-startgame": "startGame"
		},

		initialize: function(){
			this.listenTo(this.model, "change", this.render);
		},

		addBot: function(){ this.model.trigger("addBot"); },

		startGame: function(){ this.model.trigger("start"); }
	});

});
