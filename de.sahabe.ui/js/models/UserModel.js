define([
        'underscore',
        'backbone',
        'values/constants'
], function(_, Backbone,constants){

	var UserModel = Backbone.Model.extend({
		
		urlRoot : constants.settings.webServiceUrlapi+"/userdata/",
		
		defaults: {
			id: false,
			loggedIn: false,
			name: "-"
		},

		// is the user logged in or not
		isAnonymous: function() {
			return (this.get('id') == false);
		},
		
		isLoggedIn: function() {
			return this.get(loggedIn);
		}
		
	});

	// Return the model for the module
	return UserModel;

});