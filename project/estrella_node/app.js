var io = require('socket.io').listen(28553),
	http = require('http'),
	querystring = require('querystring');

io.sockets.on('connection', function(socket){
	socket.on('nodejs_ticket1', function(info){
		var values  = querystring.stringify(info);
		var opt = {
			hostname: '50.97.180.234',
			port: '32641',
			path: '/nodejs_ticket/',
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				'Content-Length': values.length
			}
		};
		var request = http.request(opt, function(res){
			res.setEncoding('utf8');
			res.on('data', function(data){
				io.sockets.emit('append-ticket', data);
			});
		});
		request.write(values);
		request.end();
	});
});
