$(function(){

	cardsAgainstHumanity.GamePlayer = Backbone.Model.extend({
		defaults: {
			score: 0
		}
	});

	cardsAgainstHumanity.GamePlayerView = Backbone.Marionette.ItemView.extend({
		template: "#template-gameplayer",

		tagName: "li"
	});

	cardsAgainstHumanity.GamePlayers = Backbone.Collection.extend({
		model: cardsAgainstHumanity.GamePlayer
	});

	cardsAgainstHumanity.GamePlayersView = Backbone.Marionette.CollectionView.extend({
		initialize: function(){
			this.listenTo(this.collection, "change", this.render);
			this.listenTo(this.collection, "add", this.render);
		},

		itemView: cardsAgainstHumanity.GamePlayerView
	});

});
