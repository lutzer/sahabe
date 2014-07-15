define([
        'underscore',
        'backbone',
        'models/LinkModel',
        'values/constants'
], function(_, Backbone, LinkModel, constants){
	
	SearchCollection = Backbone.Collection.extend({
		
		model: LinkModel,
		url : constants.settings.webServiceUrl+"/search"
		
	});
	
	return SearchCollection;
});