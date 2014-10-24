define([], function(){
	var constants = {

			settings: {
				// server settings
				webServiceUrl : "http://192.168.7.36/api",
				//webServiceUrl : "http://192.168.7.29:5000",
				webServiceLoginTimeout : 2000,
				messageDisplayTimeout : 3000
			},
	
			errors: {
				'0' : {
					title : 'Error.',
					text : 'An Unknown Error occured.'
				},
				'1' : {
					title : 'Connection Error',
					text : 'Cannot connect to server.'
				}
			}

	};
	return constants;
});