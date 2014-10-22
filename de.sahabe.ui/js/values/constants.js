define([], function(){
	var constants = {

			settings: {
				// server settings
				webServiceUrl : "http://192.168.7.29:5000",
				loginTimeout : 2000
			},
	
			errors: {
				'0' : {
					title : 'Unknown Error.',
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