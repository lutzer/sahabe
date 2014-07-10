define([
	'jquery',
	'underscore',
	'backbone',
	'models/UserModel',
	'views/HomeView',
	'views/LoginView',
	'views/UserView'
], function($, _, Backbone, UserModel, HomeView, LoginView, UserView){

	var AppRouter = Backbone.Router.extend({
		routes: {
			'login' : 'login',
			'user/:username' : 'user',
			'*actions' : 'default'
		},
	});
	
	// adds all views to #container and removes unused views
	var AppView = {
			showView: function(view) {
				if (this.currentView){
					this.currentView.close();
				}
				this.currentView = view;
				this.currentView.render();
				$("#container").append(this.currentView.el);
			}
	};

	var initialize = function(){
		
		//global models
		var user = new UserModel();
		
		//setup routes
		var app_router = new AppRouter;
		app_router.on('route:default', function(actions){
			AppView.showView(new HomeView());
		});
		app_router.on('route:login', function(actions){
			AppView.showView(new LoginView());
		});
		app_router.on('route:user', function(actions){
			AppView.showView(new UserView({username: actions}));
		});

		Backbone.history.start();
	};

	return {
		initialize: initialize
	};
});