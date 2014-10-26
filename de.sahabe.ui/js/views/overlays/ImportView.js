define([
    'jquery',
	'underscore',
	'backbone',
	'marionette',
	'vent',
	'text!templates/overlays/importTemplate.html'
], function($, _, Backbone, Marionette, vent, importTemplate){
	var ImportView = Marionette.ItemView.extend({
		
		template: _.template(importTemplate),
		
		className: 'overlay-background',
		
		events : {
			'click .closeButton' : '_onCloseButtonPress',
			'change input:file' : '_onImportFileChange'
		},
			
		_onCloseButtonPress: function() {
			this.destroy();
		},
		
		_onImportFileChange: function() {
			var self = this;
			
			var files = this.$('#importFileField')[0].files;
			var file = files[0];
			
			this.collection.importFromFile(file,onSuccess,onError);
			
			vent.trigger("display:message","Importing links... (May take some time)");
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
			
		}
		
	});
	return ImportView;
});