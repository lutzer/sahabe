define([
        'underscore',
        'backbone',
        'models/LinkModel'
], function(_, Backbone, LinkModel){
	
	LinkCollection = Backbone.Collection.extend({
		model: LinkModel
		
	});
	
	return LinkCollection;
});