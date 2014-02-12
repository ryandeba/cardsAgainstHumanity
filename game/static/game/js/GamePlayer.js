$(function(){

	cardsAgainstHumanity.GamePlayer = Backbone.Model.extend({
	});

	cardsAgainstHumanity.GamePlayerView = Backbone.View.extend({
	});

	cardsAgainstHumanity.GamePlayers = Backbone.Collection.extend({
		model: cardsAgainstHumanity.GamePlayer
	});

	cardsAgainstHumanity.GamePlayerView = Backbone.Marionette.CollectionView.extend({
	});

});
