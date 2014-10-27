define([
	'jquery',
	'underscore',
	'marionette',
], function($, _, Marionette){
	
	var KeypressBehavior = Marionette.Behavior.extend({
		
		defaults : {
			listenToKeys : {
				'13' : 'enterKeyPress',
				'27' : 'escKeyPress'
			}
		},
		
		events : {
			'keydown input' : 'onInputKeyDown'
		},
		
		onInputKeyDown : function(e) {
			
			var self = this;
			keys = Object.keys(this.options.listenToKeys);
			
			if (!e) e = window.event;
			
			keys.every(function(key) {
				if (e.keyCode == key) {
					self.view.triggerMethod(self.options.listenToKeys[key]);
					return false;
				}
				return true;
			});
		}
		
	});
	return KeypressBehavior;
	
});