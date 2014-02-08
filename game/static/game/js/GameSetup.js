$(function(){

	cardsAgainstHumanity.GameSetupView = Backbone.Marionette.ItemView.extend({
		template: "#template-gamesetup",

		events: {
			"submit .js-creategame": "createGame"
		},

		createGame: function(e){
			e.preventDefault();
			cardsAgainstHumanity.vent.trigger("createGame", {});
		}
	});

});
