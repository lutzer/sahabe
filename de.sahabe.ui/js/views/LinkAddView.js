define([
	'jquery',
	'underscore',
	'views/BaseView',
	'values/constants',
	'text!templates/linkAddTemplate.html'
], function($, _, BaseView, constants,  linkAddTemplate){
	
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
			
			var title = $('#title').val();
			var url = $('#url').val();
			var description = $('#description').val();
			
			$.ajax({
	            url: constants.settings.webServiceUrl+"/link/add",
	            type: 'PUT',
	            dataType: "json",
	            data: { title: title, url : url, description : description},
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