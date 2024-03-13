// main.js

function geocodeLocation(location, type) {
    // Use Bing Maps Location API to get the coordinates of the location.
    const geocodeRequest = `https://dev.virtualearth.net/REST/v1/Locations/${encodeURIComponent(location)}?key=AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk`;

    // Make an AJAX request to the Bing Maps Location API.
    $.ajax({
        url: geocodeRequest,
        dataType: 'json',
        success: function (data) {
            // Extract coordinates from the response.
            const coordinates = data.resourceSets[0].resources[0].point.coordinates;

            // Use the obtained coordinates for further processing.
            console.log(`${type} Location - Latitude: ${coordinates[0]}, Longitude: ${coordinates[1]}`);

            // Update the HTML with latitude and longitude information.
            updateLocationInfo(`${type.toLowerCase()}LocationInfo`, `${type} Location - Latitude: ${coordinates[0]}, Longitude: ${coordinates[1]}`);
        },
        error: function (error) {
            console.error(`Error geocoding location: ${error}`);
        }
    });
}

function updateLocationInfo(elementId, info) {
    // Update the HTML with location information.
    const infoDiv = document.getElementById(elementId);
    infoDiv.innerHTML = info;
}
