var https = require('https');

function getDirections(start, end) {
    var path = '/REST/v1/Routes/Driving?wp.0=' + encodeURIComponent(start) + '&wp.1=' + encodeURIComponent(end) + '?key=AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk';

    var options = {
        host: 'dev.virtualearth.net',
        path: path
    };

    var request = https.request(options, function(response) {
        var data = '';

        response.on('data', function(chunk) {
            data += chunk;
        });

        response.on('end', function() {
            var routeData = JSON.parse(data);
            console.log(routeData);
            // You now have the route data which you can process as needed.
        });
    });

    request.on('error', function(e) {
        console.error('Error: ' + e.message);
    });

    request.end();
}

getDirections('Seattle, WA', 'San Francisco, CA');
