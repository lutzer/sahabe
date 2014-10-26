define([
        'jquery',
        'underscore',
        'backbone',
        'models/LinkModel',
        'values/constants'
], function($,_, Backbone, LinkModel, constants){
	
	LinkCollection = Backbone.Collection.extend({
		
		model: LinkModel,
		url : constants.settings.webServiceUrl+"/links",
		
		parse : function(response) {
			return response.links;
		},
		
		deleteModels: function(models,successCallback,errorCallback) {
			var self = this;
			
			// get the linkIds of all the models to delete
			var linkIds = [];
			_.forEach(models, function(model) {
				linkIds.push(model.get('linkId'));
			});
			
			$.ajax({
	            url: self.url+"/delete",
	            type: 'POST',
	            dataType: "json",
	            data: {linkIds: linkIds },
	            success: function () {
	                _.forEach(models, function(model) {
	                	self.remove(model);
	                });
	                successCallback();
	            },
	            error: errorCallback
	        });
		},
		
		importFromFile: function(file,successCallback,errorCallback) {
			var self = this;
			
			var formData = new FormData();
			formData.append('file',file);
			
			$.ajax({
		        url: 'http://192.168.7.29:5000/links/import',  //Server script to process data
		        type: 'POST',
		        data: formData,
		        cache: false,
		        contentType: false,
		        processData: false,
		        success: successCallback,
		        error: errorCallback
		    });
		}
		
	});
	
	return LinkCollection;
});