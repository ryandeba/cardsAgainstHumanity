$(function(){

	cardsAgainstHumanity.Game = Backbone.Model.extend({
		initialize: function(){
			this.load();
		},

		load: function(){
			var self = this;
			$.ajax({
				url: "/game/" + self.get("id")
			});
		}
	});

	cardsAgainstHumanity.GameView = Backbone.Marionette.ItemView.extend({
		template: "#template-game-active"
	});

});
