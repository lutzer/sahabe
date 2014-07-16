define([
        'underscore',
        'backbone',
        'models/LinkModel',
        'values/constants'
], function(_, Backbone, LinkModel, constants){
	
	LinkCollection = Backbone.Collection.extend({
		
		model: LinkModel,
		url : constants.settings.webServiceUrl+"/links",
		
		deleteModels: function(models) {
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
	            data: {linkIds : linkIds},
	            success: function () {
	                _.forEach(models, function(model) {
	                	self.remove(model);
	                });
	            },
	            error: function(error) {
	            	console.log(error);
	            }
	        });
		}
		
	});
	
	
	
	return LinkCollection;
});