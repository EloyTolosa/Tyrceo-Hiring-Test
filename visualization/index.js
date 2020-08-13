$(function () {
    mapboxgl.accessToken = "pk.eyJ1Ijoiam1jYXJyYXNjb3NhIiwiYSI6ImNrZGlvcmIzMzA3MW0zMG50dG90NWJ0aTEifQ.ZoobdVV5OqJUUVH-k2ZHDg"
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11', 
        /* Starting position: Mallorca Center */
        center: [2.65024,39.56939],
        zoom: 9 // starting zoom
    });
    jQuery.getJSON("points.geojson", function (dat) {
        map.on('load', function () {
            // Add an image to use as a custom marker
            map.loadImage(
                'https://docs.mapbox.com/mapbox-gl-js/assets/custom_marker.png',
                function (error, image) {
                    if (error) throw error;
                    map.addImage('custom-marker', image);

                    map.addSource('points', {
                        'type': 'geojson',
                        'data': dat
                    });

                    map.addLayer({
                        'id': 'pokemons',
                        'type': 'circle',
                        'source': 'points',
                        'paint': {
                            'circle-radius': {
                                'base': 2.5,
                                'stops': [
                                    [12, 3],
                                    [22, 180]
                                ]
                            },
                            /* The dots in black show the typos and stuff. We want to keep them so we put them in a different color
                            but we can see when we look at it in the map, that belongs to a certain pokemon */
                            'circle-color': [
                                'match',
                                ['get', 'pokemon'],
                                /* Squirtle, blue color */
                                'Squirtle',
                                '#55a3ab',
                                /* Bulbasaur, turquoise green color */
                                'Bulbasaur',
                                '#a0d6b4',
                                /* Charmander, orange color */
                                'Charmander',
                                '#f15f3e',
                                /* Typos, black */
                                '#000000'
                            ]
                        }
                    });
                }
            );
        });
    });

})