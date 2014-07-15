define([
	'jquery',
	'underscore',
	'views/BaseView',
	'singletons/TheUser',
	'text!templates/homeTemplate.html'
], function($, _, BaseView, TheUser, homeTemplate){
	
	var HomeView = BaseView.extend({

		render: function(){
			
			var user = TheUser.getInstance().model;
			
			var compiledTemplate = _.template( homeTemplate, {user: user} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		}
	});
	// Our module now returns our view
	return HomeView;
	
});