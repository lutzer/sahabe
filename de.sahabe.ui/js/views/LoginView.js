define([
	'jquery',
	'underscore',
	'views/BaseView',
	'values/constants',
	'models/UserModel',
	'singletons/TheUser',
	'text!templates/loginTemplate.html'
], function($, _, BaseView, constants, UserModel, TheUser, loginTemplate){
	
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
	                //TODO: initialize singleton properly
	                /*var user = TheUser.getInstance.model;
	                user.set({'id' : data.userId});
	                user.fetch();
	                window.location.hash = "#/user/"+user.get('name');*/
	                window.location.hash = "#/user/blabla";
	                
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