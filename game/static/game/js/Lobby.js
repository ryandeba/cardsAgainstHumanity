$(function(){

	cardsAgainstHumanity.LobbyGame = Backbone.Model.extend({
	});

	cardsAgainstHumanity.LobbyGameView = Backbone.Marionette.ItemView.extend({
		template: "#template-lobbygamelistitem",

		tagName: "span"
	});

	cardsAgainstHumanity.LobbyGames = Backbone.Collection.extend({
		model: cardsAgainstHumanity.LobbyGame,

		initialize: function(){
			this.loadResults();
		},

		comparator: function(model){
			return model.get("secondsSinceLastPlayerJoined");
		},
		
		loadResults: function(){
			var self = this;
			$.ajax({
				url: "/lobby",
				success: function(response){ self.loadResultsSuccess(response); }
			});
		},

		loadResultsSuccess: function(response){
			var self = this;
			self.reset(response);
		}
	});

	cardsAgainstHumanity.LobbyGamesView = Backbone.Marionette.CompositeView.extend({
		template: "#template-lobby",

		itemView: cardsAgainstHumanity.LobbyGameView,

		itemViewContainer: ".js-lobbygames",

		events: {
			"click .js-refreshlobby": "refreshLobby",
			"click .js-newgame": "newGame",
			"submit .js-username-form": "setUsername"
		},

		refreshLobby: function(){
			this.collection.loadResults();
		},

		newGame: function(){
			cardsAgainstHumanity.vent.trigger("lobby:setupNewGame");
		},

		setUsername: function(e){
			e.preventDefault();
			var username = this.$el.find("#username").val();
			$.ajax({ url: "setPlayerName/" + username });
		}
	});

});
