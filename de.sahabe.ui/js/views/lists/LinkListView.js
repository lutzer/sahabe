define([
	'jquery',
	'underscore',
	'marionette',
	'vent',
	'views/items/LinkListItemView',
], function($, _, Marionette, vent, LinkListItemView){
	
	var LinkListView = Marionette.CollectionView.extend({
		
		childView: LinkListItemView,
		
		className: "link-list",
		
		initialize: function(options) {
			options.collection.fetch();
			
		},
		
		childEvents: {
		    'edit': function(view,model) {
		    	this.trigger('open:editLink',model);
		    }
		},
		
		_onSearchValueChanged: function(searchString) {
			var self = this;
			
			//remove whitespaces at front and back
			searchString = $.trim(searchString);
			
			if (searchString.length > 0) {
				this.collection.fetch({ 
					data: $.param({searchValue : searchString}),
					success: onSuccess,
					error: onError
				});
			} else {
				this.collection.fetch({
					success: onSuccess,
					error: onError
				});
			}
			
			function onSuccess() {
				vent.trigger("display:message","Displaying "+ self.collection.length+" search results.");
			};
			
			function onError(error) {
				vent.trigger("display:error",error);
			};
			
		}
		
		
		
	});
	// Our module now returns our view
	return LinkListView;
	
});