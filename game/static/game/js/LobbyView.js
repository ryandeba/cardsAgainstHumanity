$(function(){

	cardsAgainstHumanity.LobbyGame = Backbone.Model.extend({
	});

	cardsAgainstHumanity.LobbyGameView = Backbone.Marionette.ItemView.extend({
		template: "#template-lobbygame",

		tagName: "span",

		events: {
			"click a": "click"
		},

		click: function(e){
			e.preventDefault();
		}
	});

	cardsAgainstHumanity.LobbyGames = Backbone.Collection.extend({
		model: cardsAgainstHumanity.LobbyGame,

		initialize: function(){
			this.loadResults();
		},
		
		loadResults: function(){
			var self = this;
			$.ajax({
				url: "/lobby",
				type: "GET",
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
			"click .js-newgame": "newGame"
		},

		refreshLobby: function(){
			this.collection.loadResults();
		}
	});

});
