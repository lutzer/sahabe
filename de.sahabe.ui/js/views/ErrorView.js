define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants',
	'text!templates/errorTemplate.html'
], function($, _, Marionette, constants, errorTemplate){
	
	var ErrorView = Marionette.ItemView.extend({
		
		initialize: function(options) {
			if (options.hasOwnProperty('error')) {
				this.error = constants.errors[options.error];
				this.error.number = options.error;
			} else {
				this.error = constants.errors['0'];
				this.error.number = 0;
			}
			
			
			if (options.hasOwnProperty('message'))
				this.error.text = options.message;
		},
		
		template : _.template(errorTemplate),
		className: 'single-page',
		
		templateHelpers : function() {
			return {
				error : this.error
			};
		}
		
	});
	// Our module now returns our view
	return ErrorView;
	
});