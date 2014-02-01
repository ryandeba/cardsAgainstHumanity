$(function(){

	cardsAgainstHumanity.Game = Backbone.Model.extend({
		initialize: function(){
			this.load();
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
			this.set("gamePlayers", new GamePlayers());
			this.get("gamePlayers").url = "game/" + this.get("id") + "/gamePlayer";
			this.get("gamePlayers").reset(response.gamePlayers);

			this.set("gameRounds", new GameRounds());
			this.get("gameRounds").url = "game/" + this.get("id") + "/gameRound";
			this.get("gameRounds").reset(response.gameRounds);
		}
	});

	cardsAgainstHumanity.GameView = Backbone.Marionette.ItemView.extend({
		template: "#template-game-active"
	});

	var GamePlayer = Backbone.Model.extend({
		idAttribute: "id",

		initialize: function(){
			this.fetch();
		}
	});

	var GamePlayerView = Backbone.Marionette.ItemView.extend({
	});

	var GamePlayers = Backbone.Collection.extend({
		model: GamePlayer
	});

	var GamePlayersView = Backbone.Marionette.CollectionView.extend({
	});

	var GameRound = Backbone.Model.extend({
	});

	var GameRounds = Backbone.Collection.extend({
		model: GameRound
	});

});
