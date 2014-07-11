define([
	'jquery',
	'underscore',
	'backbone',
	'views/HomeView',
	'views/LoginView',
	'views/UserView',
	'views/LinkAddView'
], function($, _, Backbone, HomeView, LoginView, UserView, LinkAddView){

	var AppRouter = Backbone.Router.extend({
		routes: {
			'login' : 'login',
			'user/:username' : 'user',
			'link/add' : 'linkAdd',
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
		app_router.on('route:linkAdd', function(actions){
			AppView.showView(new LinkAddView());
		});

		Backbone.history.start();
	};

	return {
		initialize: initialize
	};
});