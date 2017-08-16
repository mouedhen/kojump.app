var placesAutocomplete = places({
    container: document.querySelector('#address-input'),
    language: 'fr',
    countries: ['fr']
    //useDeviceLocation: true
});
// TODO send data to the server
placesAutocomplete.on('change', function(e) { console.log(e.suggestion) });