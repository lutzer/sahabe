define([
	'underscore',
	'backbone',
], function(_, Backbone){
	var BaseView = Backbone.View.extend({
		
		id: 'view',
		
		initialize: function(args) {
			this.childviews = [];
			Backbone.View.prototype.initialize.call(this);
		},
		
		//assigns a subview
		assign : function (view, selector) {
			this.addChildView(view);
			//console.log(this.subviews);
		    view.setElement(this.$(selector)).render();
		},
		
		close: function() {
			//close subviews
			while(this.childviews.length > 0) {
				this.childviews.pop().close();
			}
			//close view
			this.remove();
			this.unbind();
		},
		
		//adds a childview, which will be deletet on close()
		addChildView: function(view) {
			if (!(_.contains(this.childviews,view))) //only add subview if its not alread added
				this.childviews.push(view);
		}
	
	});
	return BaseView;
});