// prescribing.js
//

// Open Prescribing API client library
//------------------------------------

// Clients
// -------
//
// Client code should initialize an instance with such
// options as they desire.
//
// open_prescriptions = new Scrip();

// Coding Begins
// -------------

(function(context, namespace){

    // Check to see if we're running on Node
    if(typeof process !== 'undefined' && typeof process.argv !== 'undefined' && typeof require !== 'undefined'){
        _debuglog = function(x){
            // If we're running tests, don't flood stdout
            if(_.indexOf(process.argv, 'nhs/test/js') != -1){
                return;
            }
            return;
        }
    }else{
        // By default, use a browser
        _debuglog = function(x){
            console.log(x)
        }
    }

    // Let's set up some log levels shall we?
    var log = {
        debug: _debuglog
    }

    // Let's have an application object to hang off from
    var App = new Backbone.Marionette.Application();

    // Set up some sensible defaults
    App.config = {
        // Send messages to the console?
        log: false,
        // API host
        api_host: 'prescriptions.openhealthcare.org.uk',
        // API version
        api_version: 'v1'
    }

    // Namespaces: both pleasant and good
    App.models = {}, App.collections = {}

    App.models.

    // Deal with configuration options passed in to the start method.
    App.addInitializer(function(opts){
        _.extend(App.config, options);

        // Collate the API details
        App.config.api_uri = 'http://' + App.config.api_host
                             + '/api/' + App.config.api_version + '/'

    });

    // Initialisation API -> api = new Scrip();
    var Scrip =  = context[namespace] = function(opts){
        return App.start(opts);
    }


})(this.window||exports, "Scrip")





