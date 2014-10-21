define([
        'marionette',
        'views/HeaderView',
        'views/HomeView',
        'views/SearchView'
], function(Marionette, HeaderView, HomeView, SearchView){
	
	var Controller = Marionette.Controller.extend({
		
		initialize: function(app) {
			this.app = app;
		},
			
		defaultRoute: function() {
			this.app.headerRegion.show(new HeaderView());
			this.app.mainRegion.show(new HomeView());
			console.log('default');
		},
		
		search: function(args) {
			this.app.headerRegion.show(new HeaderView());
			this.app.mainRegion.show(new SearchView({searchString: args}));
			console.log('search '+args);
		},
		
		login: function() {
			console.log('login ');
		}
		
		
	});
	
	return Controller;
});