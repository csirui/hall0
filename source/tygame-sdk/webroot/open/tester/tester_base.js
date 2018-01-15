function setScreenSize() {
	var w = parseInt($('#mwidth').val());
	var h = parseInt($('#mheight').val());
	var ww = $('#outer').width();
	var hh = $('#outer').height();

	$('#mscreen').css({
		'left' : 10,
		'top' : 10,
		'width' : w,
		'height' : h
	});

	$('#mscreen_close').css({
		'left' : 10,
		'top' : 10,
		'width' : 30,
		'height' : 30
	});

	$('#actions').css({
		'left' : w + 20,
		'top' : 10,
		'width' : ww - w - 30
	});
	$('#logger').css({
		'left' : 10,
		'top' : h + 20,
		'width' : ww - 20,
		'height' : hh - h - 40
	});
	var dsw = 0.8;
	var dsh = 0.8;
	var dw = w * dsw;
	var dh = h * dsh;
	var dl = 10 + w * ((1 - dsw) / 2);
	var dt = 10 + h * ((1 - dsh) / 2);
	$('#mdialog').css({
		'left' : dl,
		'top' : dt,
		'width' : dw,
		'height' : dh
	});

	$('#mdialog_close').css({
		'left' : dl + dw - 15,
		'top' : dt - 15,
		'width' : 30,
		'height' : 30
	});
	clearLog();
	var deviceId = $('#mdeviceid').val();
	var clientId = $('#mclientid').val();
	var appId = $('#mgameid').val();
	NativeJava.reset(appId, clientId, deviceId);
}

$(function() {
	NativeJava.init('mscreen', 'mdialog', 'muserid');
	setScreenSize();
});

function closeMe() {
	NativeJava.CloseWindow();
}

function clearLog() {
	$('#logger').html('');
}

var logi = 0
function log(args) {
	if (typeof(args) != 'string'){
		args = JSON.stringify(args);
	}
	args = args.replace(/\</g, '&lt;');
	args = args.replace(/\>/g, '&gt;');
	args = args.replace(/\\n/g, '<br>');
	logi++;
	var head = '';
	if (logi % 2 == 0) {
		head = '<span class="log_line_0">';
	} else {
		head = '<span class="log_line_1">';
	}
	var logger = $('#logger');
	logger.append(head + '[' + logi + '][' + new Date().toUTCString() + '] '
			+ args + '</span><br>');
	var h1 = logger[0].scrollHeight;
	logger.scrollTop(h1);
}
