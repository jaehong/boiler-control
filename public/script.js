(function(){

	function get_status(callback){
		$.getJSON('http://192.168.0.13:5000/?callback=?', function(r){
			callback(r);

		});
	}


	get_status(function(r){ console.log(r);});


})();