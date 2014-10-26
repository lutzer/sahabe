define([
        'jquery',
        'underscore',
        'backbone',
        'models/GroupModel',
        'values/constants'
], function($,_, Backbone, GroupModel, constants){
	
	GroupCollection = Backbone.Collection.extend({
		
		model: GroupModel,
		url : constants.settings.webServiceUrl+"/groups",
		
		parse : function(response) {
			return response.groups;
		},
		
	});
	
	return GroupCollection;
});