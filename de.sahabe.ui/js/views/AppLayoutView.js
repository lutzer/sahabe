define([
	'jquery',
	'underscore',
	'marionette',
	'views/SidebarView',
	'views/HeaderView',
	'views/lists/LinkListView',
	'text!templates/appLayoutTemplate.html'
], function($, _, Marionette, SidebarView, HeaderView, LinkListView, appLayoutTemplate){
	
	var AppLayoutView = Marionette.LayoutView.extend({
		
		template: _.template(appLayoutTemplate),
		
		initialize: function(options) {
			
			this.linkCollection = new LinkCollection();
			this.linkCollection.fetch();
			
		},
		
		regions: {
			   'sidebarRegion': '#sidebar',
			   'contentRegion': '#content',
			   'headerRegion' : '#header'
		},
		
		onRender : function() {
			// init views
			var sidebarView = new SidebarView();
			var headerView = new HeaderView();
			
			//register events
			this.listenTo(headerView,'search:changed',this._onSearchValueChanged);
			
			//render views
			this.sidebarRegion.show(sidebarView);
			this.headerRegion.show(headerView);
			this.contentRegion.show(new LinkListView({collection : this.linkCollection}));
		},
		
		_onSearchValueChanged: function(searchString) {
			var self = this;
			
			//remove whitespaces at front and back
			searchString = $.trim(searchString);
			
			console.log("search");
			
			if (searchString.length > 0) {
				this.linkCollection.fetch({ 
					data: $.param({searchValue : searchString}),
					success: function() {
						self.trigger("display:message","Found "+ self.linkCollection.length+" search results.");
					} });
			} else {
				this.linkCollection.fetch({
					success: function() {
						self.trigger("display:message","Found "+ self.linkCollection.length+" search results.");
					}
				});
			}
			
		}

	});
	return AppLayoutView;
	
});