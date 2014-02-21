$(function(){

	cardsAgainstHumanity.GameSetupView = Backbone.Marionette.ItemView.extend({
		template: "#template-gamesetup",

		events: {
			"submit .js-creategame": "createGame"
		},

		createGame: function(e){
			e.preventDefault();
			var expansionList = "";
			this.$el.find("input:checkbox:checked").each(function(){
				expansionList += $(this).val() + ",";
			});
			this.$el.find("#expansionlist").val(expansionList);
			cardsAgainstHumanity.vent.trigger("createGame", $(e.currentTarget).serialize());
		}
	});

});
