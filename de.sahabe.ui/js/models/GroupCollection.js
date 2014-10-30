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
		
		fetched : false,
		
		parse : function(response) {
			return response.groups;
		},
		
		initialize: function(options) {
			this.on('sync',function() {
				this.fetched = true;
			},this);
		}
		
	});
	
	return GroupCollection;
});