define([
        'underscore',
        'backbone',
        'values/constants'
], function(_, Backbone, constants){

	var LinkModel = Backbone.Model.extend({
		
		selectable: false,
		
		urlRoot : constants.settings.webServiceUrl+"/links",
		idAttribute: "linkId",
		
		attributes: {
			selected : false
		},
		
		setSelectable: function(selectable) {
			this.selectable = selectable;
			this.trigger("selectable");
		},
		
		setSelected: function(selected) {
			this.set({selected: selected});
		}
	});

	// Return the model for the module
	return LinkModel;

});