require.config({
	paths: {
		jquery: 'libs/jquery-2.1.1.min',
		backbone: 'libs/backbone-min',
		underscore: 'libs/underscore-min',
		marionette: 'libs/backbone.marionette.min',
		text:	'libs/plugins/text'
	}

});
// Load the app module
require(['app',], function(App){
	
	// start the app
	App.initialize();
}
);