define([
        'underscore',
        'backbone',
        'values/constants',
        'models/LinkCollection'
], function(_, Backbone, constants, LinkCollection){
	
	SearchModel = Backbone.Model.extend({
		
		urlRoot : constants.settings.webServiceUrl+"/links",
		
		defaults: {
			links : new LinkCollection(),
			tags: []
		},
		
		// function makes sure that links and tags are updated on set attribute as a collection
		set: function(attributes, options) {
			
			// reset link collection if new links are set
		    if (this.has('links') && attributes.links !== undefined) {
		    	this.get('links').reset(attributes.links);
		    	delete attributes.links;
		    }
		    
		    return Backbone.Model.prototype.set.call(this, attributes, options);
		},
		
		getLinkCollection : function() {
			return this.get('links');
		},
		
		getTagCollection : function() {
			return this.get('tags');
		}
		
	});
	
	return SearchModel;
});