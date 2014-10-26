define([
	'jquery',
	'underscore',
	'marionette',
	'utils',
	'models/LinkModel',
	'text!templates/items/linkListItemTemplate.html',
], function($, _, Marionette, Utils, LinkModel, linkListItemTemplate){
	
	var LinkListItemView = Marionette.ItemView.extend({
		
		template: _.template(linkListItemTemplate),
		
		className: 'link-item',
		
		templateHelpers: function() {
			return {
				trimString : Utils.trimString
			};

		}
		
		/*editView : false, //set to true when editing;
		
		events: {
			"click .linkEdit": "_onLinkEditClick",
			"click .linkDelete": "_onLinkDeleteClick",
			"click .linkCancelEdit": "_onLinkCancelEditClick",
			"click .linkSave": "_onLinkSaveClick",
			"change .selectBox": "_onSelectCheckbox"	
		},
		
		initialize: function() {
			this.listenTo(this.model, 'selectableChanged', this.render);
			BaseListItemView.prototype.initialize.call(this);
		},

		render: function() {
			
			var compiledTemplate;
			if (this.editView)
				compiledTemplate = _.template( linkListItemEditTemplate, { link : this.model.toJSON()} );
			else
				compiledTemplate = _.template( linkListItemTemplate, { link : this.model.toJSON(), selectable: this.model.selectable } );
			// Append our compiled template to this Views "el"
			this.$el.html( compiledTemplate );
			return this;
		},
		
		_onLinkEditClick: function() {
			//TODO: implement link details method
			this.editView = true;
			this.render();
			return false;
		},
		
		_onLinkCancelEditClick: function() {
			this.editView = false;
			this.render();
			return false;
		},
		
		_onLinkSaveClick: function() {
			
			//update values
			this.model.set({
				title: $(".linkTitle").val(),
				url: $(".linkUrl").val(),
				description: $(".linkDescription").val()
			});
			
			// save model to database
			this.model.save(null, {
				error: function(model, response) {
					console.log(response);
				}
			});
			
			//re-render itemview
			this.editView = false;
			this.render();
			return false;
		},
		
		_onLinkDeleteClick: function() {
			this.model.destroy();
			return false;
		},
		
		_onSelectCheckbox: function() {
			this.model.set({selected : $(".selectBox").is(":checked")});
			return false;
		}*/
	});
	// Our module now returns our view
	return LinkListItemView;
	
});