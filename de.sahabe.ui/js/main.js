require.config({
	paths: {
		jquery: 'libs/jquery-2.1.1.min',
		backbone: 'libs/backbone',
		underscore: 'libs/underscore-min'
	}

});
// Load the app module
require(['app',], function(App){
   
	// start the app
	App.initialize();
});
