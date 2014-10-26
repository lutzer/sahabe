define([
	'jquery',
	'underscore',
	'marionette',
	'vent',
	'models/LinkCollection',
	'models/GroupCollection',
	'views/subviews/SidebarView',
	'views/subviews/HeaderView',
	'views/lists/LinkListView',
	'views/overlays/ImportView',
	'text!templates/appLayoutTemplate.html'
], function($, _, Marionette, vent, LinkCollection, GroupCollection, SidebarView, HeaderView, LinkListView, ImportView, appLayoutTemplate){
	
	var AppLayoutView = Marionette.LayoutView.extend({
		
		template: _.template(appLayoutTemplate),
		
		initialize: function(options) {
			this.linkCollection = new LinkCollection();
			this.groupCollection = new GroupCollection();
		},

		regions: {
			'sidebarRegion': '#sidebar',
			'contentRegion': '#content',
			'headerRegion' : '#header',
			'overlayRegion': '#overlay'
		},

		onRender : function() {
			// init views
			var headerView = new HeaderView();
			var sidebarView = new SidebarView({ groupCollection : this.groupCollection});
			var linkListView = new LinkListView({ collection : this.linkCollection});
			
			//register events
			linkListView.listenTo(headerView,'search:changed',linkListView._onSearchValueChanged);
			this.listenTo(sidebarView,'open:importFile',this.showImportOverlay);
			
			//render views
			this.sidebarRegion.show(sidebarView);
			this.headerRegion.show(headerView);
			this.contentRegion.show(linkListView);
		},
		
		showImportOverlay: function() {
			this.overlayRegion.show(new ImportView({collection : this.linkCollection}));
		}
		
	});
	return AppLayoutView;
	
});