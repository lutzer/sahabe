define([
	'jquery',
	'underscore',
	'views/BaseView',
	'values/constants',
	'models/UserModel',
	'text!templates/loginTemplate.html'
], function($, _, BaseView, constants, UserModel, loginTemplate){
	
	var LoginView = BaseView.extend({
		
		events : {
			'click .loginButton' : '_onClickLoginButton'
		},
		
		initialize: function() {
			BaseView.prototype.initialize.call(this);
		},

		render: function(){
			var compiledTemplate = _.template( loginTemplate, {} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		},
		
		_onClickLoginButton: function() {
			
			var self = this;
		
			var userData = {
				username: $('#username').val(),
				password: $('#password').val(),
				remember: $('#remember').is(":checked")
			};
		
			
			$.ajax({
	            url: constants.settings.webServiceUrl+"/login",
	            type: 'POST',
	            dataType: "json",
	            data: userData,
	            success: function (data) {
	                console.log("login succesfull:");
	                console.log(data);
	                window.location.hash = "#/user/"+userData.username;
	                
	            },
	            error: function(error) {
	            	console.log("login failed");
	            	console.log(error);
	            }
	        });
		}
	});
	// Our module now returns our view
	return LoginView;
	
});