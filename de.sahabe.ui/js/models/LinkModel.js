define([
        'underscore',
        'backbone',
        'values/constants'
], function(_, Backbone, constants){

	var LinkModel = Backbone.Model.extend({
		
		urlRoot : constants.settings.webServiceUrl+"/links",
		idAttribute: "linkId",
		
		selectable : false,
		
		attributes: {
			selected : false
		},
		
		setSelectable: function(selectable) {
			this.selectable = selectable;
			this.trigger("selectableChanged");
		},
		
		setSelected: function(selected) {
			this.set({selected: selected});
		}
	});

	// Return the model for the module
	return LinkModel;

});