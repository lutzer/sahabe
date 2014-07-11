define([
	'jquery',
	'underscore',
	'views/BaseView',
	'text!templates/linkAddTemplate.html'
], function($, _, BaseView, linkAddTemplate){
	
	var LinkAddView = BaseView.extend({
		
		events : {
			'click .addLinkButton' : '_onClickAddLinkButton'
		},

		render: function(){
			var compiledTemplate = _.template( linkAddTemplate, {} );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		},
		
		_onClickAddLinkButton: function() {
			
			var username = $('#username').val();
			var password = $('#password').val();
			var remember = $('#remember').is(":checked");
			
			$.ajax({
	            url: constants.settings.webServiceUrl+"/login",
	            type: 'POST',
	            dataType: "json",
	            data: { username: username, password : password, remember : remember},
	            success: function (data) {
	                console.log("link added");
	                console.log(data);
	                
	            },
	            error: function(error) {
	            	console.log("failed to add link");
	            	console.log(error);
	            }
	        });
		}
	});
	// Our module now returns our view
	return LinkAddView;
	
});