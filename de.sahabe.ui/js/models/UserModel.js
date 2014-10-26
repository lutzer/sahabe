define([
        'jquery',
        'underscore',
        'backbone',
        'values/constants'
], function($,_, Backbone,constants){

	var UserModel = Backbone.Model.extend({
		
		urlRoot : constants.settings.webServiceUrl+"/user/data",
		
		loggedIn : false,
		
		// override parse
		parse : function(response) {
			return response.user;
		},
		
		// override fetch
		fetch : function(options) {
			options.timeout = constants.settings.webServiceLoginTimeout;
			Backbone.Model.prototype.fetch.call(this,options);
		},
		
		validate : function(attrs, options) {
			
			errors = [];
			
			if (!(attrs.username).match("^[a-zA-Z0-9_-]{3,64}$"))
				errors.push({attr: 'username', msg: "Username is not valid"});
			if (!(attrs.email).match("[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\\.[a-zA-Z]+"))
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
		
		// checks if user is logged in
		checkLogin: function(successCallback,errorCallback) {
        	var self = this;

        	if (this.has('id')) { //if model already fetched
        		successCallback();
        	} else { // else fetch model
        		self.fetch({success : onSuccess, error: onError});
        		
        		function onSuccess(data) {
        			this.loggedIn = true;
            		successCallback();
            	};
            	
            	function onError(model,error) {
            		errorCallback(error);
            	};
        	}
        },
		
		login : function(username, password, remember, successCallback, errorCallback) {
			var self = this;
			
			var data = { username : username, password : password, remember : remember };
			
			$.ajax({
	            url: constants.settings.webServiceUrl+"/login",
	            type: 'POST',
	            dataType: "json",
	            data: data,
	            timeout: constants.settings.webServiceLoginTimeout,
	            success: successCallback,
	            error: errorCallback
	        });
		},
		
		logout : function(successCallback, errorCallback) {
			$.ajax({
	            url: constants.settings.webServiceUrl+"/logout",
	            type: 'GET',
	            timeout: constants.settings.webServiceLoginTimeout,
	            success: successCallback,
	            error: errorCallback
	        });
		},
		
		signup : function(successCallback, errorCallback) {
			
			var self = this;
			
			$.ajax({
	            url: constants.settings.webServiceUrl+"/sign_up",
	            type: 'POST',
	            dataType: "json",
	            data: self.attributes,
	            timeout: constants.settings.webServiceLoginTimeout,
	            success: successCallback,
	            error: errorCallback
	        });
		},

		// is the user logged in or not
		isLoggedIn: function() {
			return this.get('loggedIn');
		}
		
	});

	// Return the model for the module
	return UserModel;

});