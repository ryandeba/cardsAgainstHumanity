$(function(){

	cardsAgainstHumanity.Game = Backbone.Model.extend({
		defaults: {
			active: 0,
			gamePlayers: undefined,
			gameRounds: undefined
		},

		initialize: function(){
			this.set("gamePlayers", new GamePlayers());
			this.get("gamePlayers").url = "game/" + this.get("id") + "/gamePlayer";
			this.set("gameRounds", new GameRounds());
			this.get("gameRounds").url = "game/" + this.get("id") + "/gameRound";

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
			this.get("gamePlayers").reset(response.gamePlayers);

			this.get("gameRounds").reset(response.gameRounds);
		}
	});

	cardsAgainstHumanity.GameView = Backbone.View.extend({
		initialize: function(){
			//this.listenTo(this.model, "change", this.render);
		},

		template: _.template($("#template-game-active").html()),

		render: function(){
			this.$el.html(this.template(this.model.toJSON()));
			//this.renderGamePlayers();
			return this;
		},

		renderGamePlayers: function(){
			var self = this;
			var gamePlayersView = new GamePlayersView({
				collection: self.model.get("gamePlayers"),
				el: self.$el.find(".js-gameplayers")
			});
		}
	});

	var GamePlayer = Backbone.Model.extend({
		idAttribute: "id",

		initialize: function(){
			this.fetch();
		}
	});

	var GamePlayerView = Backbone.Marionette.ItemView.extend({
		template: "#template-gameplayer"
	});

	var GamePlayers = Backbone.Collection.extend({
		model: GamePlayer
	});

	var GamePlayersView = Backbone.Marionette.CollectionView.extend({
		itemView: GamePlayerView
	});

	var GameRound = Backbone.Model.extend({
	});

	var GameRounds = Backbone.Collection.extend({
		model: GameRound
	});

});
