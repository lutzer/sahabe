define([
	'jquery',
	'underscore',
	'backbone',
	'marionette',
	'controller'
], function($, _, Backbone, Marionette, Controller) {
	
	var App = new Backbone.Marionette.Application();

	var initialize = function(){
		
		App.addRegions({
			headerRegion: "#header",
			contentRegion: "#content",
			sidebarRegion: "#sidebar"
		});
		
		App.addInitializer(function(options){
			  Backbone.history.start();
		});
		
		App.Router = new Marionette.AppRouter({
			controller: new Controller(App),
			appRoutes: {
				'login' : 'login',
				'signup' : 'signup',
				'home' : 'home',
				'*actions' : 'defaultRoute'
			}
		});
		
		App.start();
		
		//setup routes
		/*var app_router = new AppRouter;
		app_router.on('route:default', function(actions){
			AppView.showView(new HomeView());
		});
		app_router.on('route:login', function(actions){
			AppView.showView(new LoginView());
		});
		app_router.on('route:search', function(searchString){
			if (searchString == null)
				searchString = "";
			AppView.showView(new SearchView({searchString : searchString}));
		});
		app_router.on('route:user', function(username){
			AppView.showView(new UserView({username: username}));
		});
		app_router.on('route:linkAdd', function(actions){
			AppView.showView(new LinkAddView());
		});

		Backbone.history.start();*/
	};
	
	
	//setup credentials to allow cross origin access
	$.ajaxSetup({
		cache: false,
		crossDomain: true,
		xhrFields: {
	        withCredentials : true
	    }
	    //timeout: 2000
	});
	$.support.cors=true;
	

	return {
		initialize: initialize
	};
	
});