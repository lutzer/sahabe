define([
	'jquery',
	'underscore',
	'marionette',
	'vent',
	'values/constants',
	'singletons/User',
	'text!templates/loginTemplate.html'
], function($, _, Marionette, vent, constants, User, loginTemplate){
	
	var LoginView = Marionette.ItemView.extend({
		
		template :  _.template( loginTemplate),
		className: 'single-page',
		
		events : {
			'click .loginButton' : '_onClickLoginButton',
			'click .signupButton' : '_onClickSignupButton',
			'keyup input' : '_onInputEnterPress'
		},
		
		onRender : function() {
			var self = this;
			_.defer(function(){ self.$('#username').focus(); });
			
		},

		
		_onClickLoginButton: function() {
			var self = this;
		
			var username = $('#username').val();
			var	password = $('#password').val();
			var	remember = $('#remember').is(":checked");
			
			var user = User.getInstance();
			
			user.model.login(username,password,remember,onSuccess,onError);
			
			vent.trigger('display:message',"Logging in...");
			
			function onSuccess() {
				vent.trigger('display:message',"Login succesfull!");
				window.location = "#";
			};
			
			function onError(error) {
				
				if (error.status == 401)
					vent.trigger('display:message',error.responseJSON.message);
				else
					vent.trigger('display:error',1,error);
				
			}
		},
		
		_onInputEnterPress: function(e) {
			if (!e) e = window.event;
		    var keyCode = e.keyCode || e.which;
		    if (keyCode == '13'){ //enter press
		    	
		    	this._onClickLoginButton();
				
			    return false;
		    }
		},
		
		_onClickSignupButton: function () {
			window.location = "#signup";
		}
		
	});
	// Our module now returns our view
	return LoginView;
	
});