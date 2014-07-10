define([
	'jquery',
	'underscore',
	'views/BaseView',
	'text!templates/homeViewTemplate.html'
], function($, _, BaseView, homeViewTemplate){
	
	var HomeView = BaseView.extend({

		render: function(){
			var compiledTemplate = _.template( homeViewTemplate, {} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		}
	});
	// Our module now returns our view
	return HomeView;
	
});