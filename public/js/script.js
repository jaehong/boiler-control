(function(){

	$('body').formplate();

	var host = 'http://192.168.0.13:5000';
	
	function get_status(callback){
		$.getJSON(host + '/?callback=?', function(r){
			callback(r);
		});
	}
	
	function get_schedule(callback){
		$.getJSON(host + '/get_schedule?callback=?', function(r){
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
		$.getJSON(host + '/'+s+'?callback=?', function(r){
			$('.status').html(r.status);
		});
	});

	$('#save').on('click', function(){
		alert('구현중입니다.');
		// validate, 정리 
		// save
	});

	get_status(function(r){
		console.log(r.status);
		$('.status').html(r.status);
		set_status(r.status);
	});

	get_schedule(function(r){

	});

})();