define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'text!templates/errorTemplate.html'
], function($, _, Marionette, constants, errorTemplate){
	
	var ErrorView = Marionette.View.extend({
		
		initialize: function(options) {
			if (options.error !== 'undefined') {
				this.error = constants.errors[options.error];
				this.error.number = options.error;
			} else {
				this.error = constants.errors['0'];
				this.error.number = 0;
			}
				
		},

		render: function(){
			var compiledTemplate = _.template( errorTemplate, {error : this.error} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		}
	});
	// Our module now returns our view
	return ErrorView;
	
});