define([
        'underscore',
        'backbone',
        'values/constants'
], function(_, Backbone, constants){

	var LinkModel = Backbone.Model.extend({
		
		urlRoot : constants.settings.webServiceUrl+"/links",
		idAttribute: "linkId",
		
		defaults: {
			title: '',
			url : '',
			description: '',
			modifiedAt: 0,
		},
		
		validate : function(attrs, options) {
			
			errors = [];
			
			if (!(attrs.url).match("^(http|ftp)s?:\\/\\/.+$"))
				errors.push({attr: 'url', msg: "url is not valid"});
			if (!(attrs.title).length > 0)
				errors.push({attr: 'title', msg: "title is empty"});
			
			if (errors.length > 0)
				return errors;
		}
		
		/*selectable : false,
		
		attributes: {
			selected : false
		},
		
		setSelectable: function(selectable) {
			this.selectable = selectable;
			this.trigger("selectableChanged");
		},
		
		setSelected: function(selected) {
			this.set({selected: selected});
		}*/
	});

	// Return the model for the module
	return LinkModel;

});