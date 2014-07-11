define([
	'jquery',
	'underscore',
	'views/BaseView',
	'text!templates/homeTemplate.html'
], function($, _, BaseView, homeTemplate){
	
	var HomeView = BaseView.extend({

		render: function(){
			
			var compiledTemplate = _.template( homeTemplate, {} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		}
	});
	// Our module now returns our view
	return HomeView;
	
});