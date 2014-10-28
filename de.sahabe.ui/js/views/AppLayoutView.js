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
	'views/overlays/LinkEditView',
	'views/overlays/LinkAddView',
	'views/overlays/GroupEditView',
	'text!templates/appLayoutTemplate.html'
], function($, _, Marionette, vent, LinkCollection, GroupCollection, SidebarView, HeaderView, LinkListView, ImportView, LinkEditView, LinkAddView, GroupEditView, appLayoutTemplate){
	
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
			
			//register direct view events
			linkListView.listenTo(headerView,'search:changed',linkListView._onSearchValueChanged);
			this.listenTo(sidebarView,'open:importFile',this.showImportOverlay);
			this.listenTo(headerView,'open:addLink', this.showLinkAddOverlay);
			
			//register indirect view events
			vent.on("open:editGroup",this.showGroupEditOverlay,this);
			vent.on("open:editLink",this.showLinkEditOverlay,this);
			
			//render views
			this.sidebarRegion.show(sidebarView);
			this.headerRegion.show(headerView);
			this.contentRegion.show(linkListView);
		},
		
		showImportOverlay: function() {
			this.overlayRegion.show(new ImportView({collection : this.linkCollection}));
		},
		
		showLinkEditOverlay: function(model) {
			this.overlayRegion.show(new LinkEditView({model : model}));
		},
		
		showLinkAddOverlay: function() {
			this.overlayRegion.show(new LinkAddView({collection : this.linkCollection}));
		},
		
		showGroupEditOverlay: function(model) {
			this.overlayRegion.show(new GroupEditView({model : model}));
		}
		
	});
	return AppLayoutView;
	
});