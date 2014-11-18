(function(){

	$('body').formplate();

	var host = document.location.origin;

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
		$('.status').html('작동중 ');
		$.getJSON(host + '/'+s+'?callback=?', function(r){
			$('.status').html(r.result);
		});
	});

	$('#save').on('click', function(){
		var s = $('#schedule').val().trim().split("\n");
		var processed = [];
		var valid = 0;
		s.forEach(function(item){
			item = item.trim();
			valid += /^[0-9]{2}:[0-9]{2}\s[켬|끔]/.test(item);
			processed.push(item);
		});
		if(valid != s.length){
			alert("표현을 확인하세요. \n01:00 켬\n같은 형식입니다.");
			$('#schedule').focus();
			return false;
		}
		$('#schedule').val(processed.join("\n"));
		var processed = processed.join("\\n");
		$.post(host + '/set_schedule', {data: processed}, function(r){
			alert(r);
		});
	});

	get_status(function(r){
		console.log(r.result);
		$('.status').html(r.result);
		set_status(r.result);
	});

	get_schedule(function(r){
		$('#schedule').val(r.result);
	});

})();