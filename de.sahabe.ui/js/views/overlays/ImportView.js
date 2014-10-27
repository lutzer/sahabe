define([
    'jquery',
	'underscore',
	'backbone',
	'marionette',
	'vent',
	'behaviors/KeypressBehavior',
	'text!templates/overlays/importTemplate.html'
], function($, _, Backbone, Marionette, vent, KeypressBehavior, importTemplate){
	var ImportView = Marionette.ItemView.extend({
		
		template: _.template(importTemplate),
		
		className: 'overlay-background',
		
		events : {
			'click .closeButton' : 'onCloseButtonPress',
			'change input:file' : 'onImportFileChange'
		},
		
		behaviors: {
		    keypressBehavior: {
		        behaviorClass: KeypressBehavior
		    }
		},
			
		onCloseButtonPress: function() {
			this.destroy();
		},
		
		onImportFileChange: function() {
			var self = this;
			
			var files = this.$('#importFileField')[0].files;
			var file = files[0];
			
			this.collection.importFromFile(file,onSuccess,onError);
			
			vent.trigger("display:message","Importing links... May take a few minutes.");
			self.destroy();
			
			//TODO: return how many links got imported
			function onSuccess() {
				vent.trigger("display:message","Links succesfully imported.");
				//TODO: use current search string to fetch collection again
				self.collection.fetch();
			};
			
			function onError(error) {
				vent.trigger("display:message","Failed importing bookmarks from file.");
			};
			
		},
		
		onEscKeyPress: function() {
			this.onCloseButtonPress();
		}
		
	});
	return ImportView;
});