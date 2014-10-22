define([
        'jquery',
        'underscore',
        'backbone',
        'values/constants'
], function($,_, Backbone,constants){

	var UserModel = Backbone.Model.extend({
		
		urlRoot : constants.settings.webServiceUrl+"/user/data",
		
		defaults: {
			loggedIn: false,
			name: "-"
		},
		
		// override fetch
		fetch : function(options) {
			options.timeout = constants.settings.loginTimeout;
			Backbone.Model.prototype.fetch.call(this,options);
		},
		
		validate : function(attrs, options) {
			
			errors = [];
			
			if (!(attrs.username).match("^[a-z0-9_-]{3,15}$"))
				errors.push({attr: 'username', msg: "Username is not valid"});
			if (!(attrs.email).match(/@/))
				errors.push({attr: 'email', msg: "Email is not valid"});
			if (attrs.password.length < 6) {
				errors.push({attr: 'password', msg: "Password has to be 6 characters long"});
				errors.push({attr: 'password2', msg: "Password has to be 6 characters long"});
			}
			if (attrs.password != attrs.password2)
				errors.push({attr: 'password2', msg: "Passwords do not match"});
			
			if (errors.length > 0)
				return errors;
		},
		
		login : function(username, password, remember, successCallback, errorCallback) {
			var self = this;
			
			var data = { username : username, password : password, remember_me : remember };
			
			$.ajax({
	            url: constants.settings.webServiceUrl+"/user/login",
	            type: 'POST',
	            dataType: "json",
	            data: data,
	            timeout: constants.settings.loginTimeout,
	            success: function (data) {
	            	self.set(data);
	            	successCallback();
	            },
	            error: function(error) {
	            	errorCallback();
	            }
	        });
		},
		
		logout : function() {
			
		},
		
		signup : function(successCallback, errorCallback) {
			errorCallback();
		},

		// is the user logged in or not
		isLoggedIn: function() {
			return this.has('id');
		}
		
	});

	// Return the model for the module
	return UserModel;

});