define([
    'jquery',
	'underscore',
	'backbone',
	'views/BaseView'
], function($,_, Backbone,BaseView){
	var BaseOverlay = BaseView.extend({
		
		el : '',
		id: 'overlay',
		parent: false,
		
		initialize: function(options) {

			this.visible = false;
			//this.parent = options.parent;
			
			//append to body
			if (!( $( "#overlay" ).length))
				$('#container').append(this.el);
			
			this.hide();
			
			BaseView.prototype.initialize.call(this);
		},
		
		show: function() {
			this.visible = true;
			this.render();
			$(this.el).show();
		},
		
		hide: function() {
			this.visible = false;
			$(this.el).hide();
		},
		
	});
	return BaseOverlay;
});