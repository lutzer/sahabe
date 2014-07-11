define([
        'underscore',
        'backbone',
        'models/LinkModel',
        'values/constants'
], function(_, Backbone, LinkModel, constants){
	
	LinkCollection = Backbone.Collection.extend({
		
		model: LinkModel,
		url : constants.settings.webServiceUrl+"/links"
		
	});
	
	return LinkCollection;
});