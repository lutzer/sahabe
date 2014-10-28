define([
        'marionette',
        'vent',
        'utils',
        'singletons/User',
        'views/AppLayoutView',
        'views/LoginView',
        'views/SignupView',
        'views/ErrorView',
        'views/MessageView'
], function(Marionette, Vent, Utils, User, AppLayoutView, LoginView, SignupView, ErrorView, MessageView){
	
	var Controller = Marionette.Controller.extend({
		
		initialize: function(app) {
			this.app = app;
			
			// register events
			Vent.on('display:message', this.showMessage,this);
			Vent.on("display:error", this.showErrorPage,this);
		},
		
		// checks if user is logged in, callback returns true if logged in, false otherwise
		checkLogin: function(callback) {
			var self = this;
			
			var user = User.getInstance();
			user.model.checkLogin(onSuccess,onError);
			
			function onSuccess() {
				callback(true);
			};
			
			function onError(error) {
				if (error.status == 401)
					callback(false);
				else
					Vent.trigger("display:error",1,error)
			};
		},
		
		// displays an errorPage
		showErrorPage: function(errorId,error) {
			if (Utils.propertyExists(error,"responseJSON.message"))
				this.app.containerRegion.show(new ErrorView({error : errorId, message : error.responseJSON.message}));
			else
				this.app.containerRegion.show(new ErrorView({error : errorId}));
			//window.location = "#error/"+errorId;
		},
		
		// displays a message to the user
		showMessage: function(message) {
			this.app.messageRegion.show(new MessageView({message : message}));
		},
			
		/* ROUTES */
		
		home: function(searchText) {
			
			if (typeof searchText == 'undefined')
				searchText = false;
			
			var self = this;
			
			this.checkLogin(
				function(loggedIn) {
					if (loggedIn) {
						self.app.containerRegion.show(new AppLayoutView({searchText : searchText}));
					} else
						window.location = "#login";
				}
			);
		},
		
		login: function() {
			this.app.containerRegion.show(new LoginView());
		},
		
		logout: function() {
			
			var user = User.getInstance();
			user.model.logout(onSuccess,onError);
			
			function onSuccess(response) {
				Vent.trigger("display:message",response.message);
				
				var user = User.getInstance();
				user.reset();
				
				window.location="#";
			};
			
			function onError(error) {
				if (error.status != 401)
					Vent.trigger("display:error",1,error)
				else
					window.location="#";
			};
		},
		
		signup: function() {
			this.app.containerRegion.show(new SignupView());
		},
		
		user: function(name) {
			alert("Userview for "+name);
		},
		
		error: function(errorId) {
			this.app.containerRegion.show(new ErrorView({error : errorId}));
		},
		
		defaultRoute: function() {
			this.home();
		},
		
		
		
	});
	
	return Controller;
});