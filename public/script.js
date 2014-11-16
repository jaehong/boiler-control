(function(){

	function get_status(callback){
		$.getJSON('http://192.168.0.13:5000/?callback=?', function(r){
			callback(r);
		});
	}

	$('.buttons button').on('click', function(e){
		var s = e.currentTarget.innerHTML.toLowerCase();
		$.getJSON('http://192.168.0.13:5000/'+s+'?callback=?', function(r){
			$('.status').html(r.status);
		});
	});

	get_status(function(r){
		console.log(r.status);
		$('.status').html(r.status);
	});


})();