define([
	'jquery',
	'underscore',
	'marionette',
	'values/constants'
], function($, _, Marionette, constants){
	
	var ValidationBehavior = Marionette.Behavior.extend({
		
		defaults : {
			idPrefix : ''
		},
		
		modelEvents: {
		      "invalid": "handleInvalidModelError"
		},
		
		
		onValidateForm : _.debounce(function(event) {
			
			if (typeof event !== 'undefined')
				this.view.$(event.target).removeClass('invalid');
			this.view.model.isValid();
		},constants.settings.inputDebounceTime),
		
		handleInvalidModelError: function(model, errors) {
			var self = this;
			
			_.each(errors,function(error) {
				self.view.$('#' + self.options.idPrefix + error.attr).addClass('invalid');
			});
			
		}
		
	});
	return ValidationBehavior;
	
});