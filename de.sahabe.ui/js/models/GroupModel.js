define([
        'underscore',
        'backbone',
        'values/constants'
], function(_, Backbone, constants){

	var GroupModel = Backbone.Model.extend({
		
		urlRoot : constants.settings.webServiceUrl+"/groups",
		idAttribute: "id",
		
		defaults : {
			public : false
		},
		
		validate : function(attrs, options) {
			
			errors = [];
			
			if (!(attrs.name).match("^[a-zA-Z0-9_-\\s]+$"))
				errors.push({attr: 'name', msg: "Groupname not valid"});
		
			if (errors.length > 0)
				return errors;
		},
		
		
	});

	// Return the model for the module
	return GroupModel;

});