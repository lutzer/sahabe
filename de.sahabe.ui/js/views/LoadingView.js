define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'text!templates/loadingTemplate.html'
], function($, _, Marionette, constants, loadingTemplate){
	
	var LoadingVIew = Marionette.View.extend({
		
		initialize: function(options) {
				
		},

		render: function(){
			var compiledTemplate = _.template( loadingTemplate );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		}
	});
	// Our module now returns our view
	return LoadingVIew;
	
});