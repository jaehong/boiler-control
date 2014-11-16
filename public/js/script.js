(function(){

	$('body').formplate();

	function get_status(callback){
		$.getJSON('http://192.168.0.13:5000/?callback=?', function(r){
			callback(r);
		});
	}

	function set_status(status){
		if(status==='on'){
			$('.checkbox .fp-toggler').addClass('checked');
			$('#status').attr('checked', true);
		} else {
			$('.checkbox .checked').removeClass('checked');
			$('#status').prop('checked',false);
		}		
	}

	$('.checkbox .fp-toggler').on('click', function(e){
		var s = e.currentTarget.classList.contains('checked') ? 'off' : 'on';
		$.getJSON('http://192.168.0.13:5000/'+s+'?callback=?', function(r){
			$('.status').html(r.status);
		});
	});


	get_status(function(r){
		console.log(r.status);
		$('.status').html(r.status);
		set_status(r.status);
	});



})();