define([
	'jquery',
	'underscore',
	'views/BaseView',
	'models/LinkModel',
	'values/constants',
	'text!templates/linkAddTemplate.html'
], function($, _, BaseView, LinkModel, constants,  linkAddTemplate){
	
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
			
			var link = new LinkModel({title: title, url : url, description : description});
			link.save(null,{
				error: function(model, response) {
					console.log(model);
					console.log(response);
				}
			});
			
			
		}
	});
	// Our module now returns our view
	return LinkAddView;
	
});