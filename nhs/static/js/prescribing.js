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

    // Let's sort out our dependencies
    if (typeof $ === 'undefined'&& (typeof require !== 'undefined')){
        $ = require('jquery');
    }
    if (typeof _ === 'undefined'&& (typeof require !== 'undefined')){
        _ = require('underscore');
    }
    if (typeof Backbone === 'undefined'&& (typeof require !== 'undefined')){
        Backbone = require('backbone');
    }

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

    // Namespace mapping functions
    var mapping = {

        info: null,
        geojson: null,

        // Make a blank CCG feature
        CCGFeature: function(){
            feat = {
                type: 'Feature',
                properties: {
                    ccg_code: null,
                    Name: null,
                    ccg_name: null,
                    total_items_month: null,
                    Description: null,
                    ccg_problem: null,
                    pop_per_surgery: null,
                    no_of_practices: null,
                    no_of_lsoas: null,
                    population: null,
                    region: null
                },
                geometry: null
            }
            return feat;
        },

        initialize: function(identifier){
            var map = L.map(identifier).setView([53.0, -1.5], 6);
            var cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
                key: 'BC9A493B41014CAABB98F0471D759707',
                styleId: 22677
            }).addTo(map);
            return map;
        },

        // get color depending on the value we're heatmapping
        getColor: function(d) {
            return d > 27  ? '#990000' :
                d > 25  ? '#D7301F' :
                d > 24  ? '#EF6548' :
                d > 23  ? '#FC8D59' :
                d > 22  ? '#FDBB84' :
                d > 21  ? '#FDD49E' :
                d > 19  ? '#FEE8C8' :
                '#FFF7EC';
        },

        // Style of an individual layer
        style: function(feature) {
            return {
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7,
                fillColor: mapping.getColor(feature.properties.ccg_problem)
            };
        },

        // Highlight an individual feature
        highlightFeature: function(e) {
            var layer = e.target;
            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            });

            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToFront();
            }
            mapping.info.update(layer.feature.properties);
        },

        // return our feature to normal
        resetHighlight: function(e) {
            // TODO - FIX THIS
            mapping.geojson.resetStyle(e.target);
            mapping.info.update();
        },

        // When we've selected a feature, zoom to it.
        zoomToFeature: function(e) {
            map.fitBounds(e.target.getBounds());
        },

        onEachFeature: function(feature, layer) {
            layer.on({
                mouseover: mapping.highlightFeature,
                mouseout: mapping.resetHighlight,
                click: mapping.zoomToFeature
            });
        },

        // control that shows state info on hover
        make_hoverinfo: function(map){
            var info = L.control();
            mapping.info = info;

            // Create a DOM element
            info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info');
                this.update();
                return this._div;
            };

            // Fill our DOM element
            info.update = function (props) {
                this._div.innerHTML = '<h4>Drug Explorer</h4>'
                    +  (props ? '<b>CCG: ' + props.ccg_name + '</b><br />'
                        + props.ccg_problem.toFixed(2) + '%'
                        + '<br />' + props.total_items_month + ''
                        + '<br />' + props.population + ' population'
                        + '<br />' + props.no_of_practices + ' GP Practices'
                        : 'Hover over a CCG');
            };
            info.addTo(map);
        },

        // Add legends and metadata to our map
        make_legend: function(map){
            var geojson;
            var legend = L.control({position: 'bottomright'});
            legend.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'info legend'),
                grades = [0, 19, 21, 22, 23, 24, 25, 27, 35], // [0, 10, 20, 50, 100, 200, 500, 1000],
                labels = [],
                from, to;

                for (var i = 0; i < grades.length; i++) {
                    from = grades[i];
                    to = grades[i + 1];

                    labels.push(
                        '<i style="background:' + mapping.getColor(from + 1) + '"></i> ' +
                            from + (to ? '&ndash;' + to : '+'));
                }

            div.innerHTML = labels.join('<br>');
                return div;
            };
            legend.addTo(map);

        }
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
        api_version: 'v1',

        // Collate the API details
        api_uri: function(){
            return 'http://' + App.config.api_host
                + '/api/' + App.config.api_version + '/'
        }

    }

    // Define our own generic collection
    ScripCollection = Backbone.Collection.extend({

        // Build this from the options hash
        url: function(){
            return App.config.api_uri() + this.resource + '/'
        },

        // Ignore the Metadata that Tastypie returns
        parse: function(response, options){
            log.debug("API response");
            log.debug(response);
            return response.objects || response;
        }

    });

    // Define our models
    Practice = Backbone.Model.extend({});
    Drug     = Backbone.Model.extend({});
    Bucket   = Backbone.Model.extend({});

    // Define Collections
    Pharmacy = ScripCollection.extend({
        model: Drug,
        resource: 'product'
    });

    Brigade = ScripCollection.extend({
        model: Bucket,
        resource: 'prescriptioncomparison',
    });

    // Views
    OPMap = Backbone.Marionette.ItemView.extend({
        template: function(serialised_model){
            var markup = "<center><div id=\"map\"><img src=\"https://s3-eu-west-1.amazonaws.com/prescribinganalytics/img/spinner.gif\" style='margin-top:20px;'></div></center>"
            return markup
        }
    });

    BucketMap = OPMap.extend({

        initialize: function(opts){
            this.collection = opts.collectoin;
            this.on('show', this.render_map,  this);
            opts.collection.on('reset', this.item_added, this);
        },

        // The View's markup has been rendered into the view, so
        // we're good to create the map with our JS
        render_map: function(){
            log.debug('render_map called')
            map = mapping.initialize('map')
            mapping.make_hoverinfo(map)
            mapping.make_legend(map)
            this.map = map;
        },

        // Given our buckets from the API. parse these into map Features,
        // matching them to our CCG geometry data
        parse_buckets: function(ccgGeoms, brigade){
            log.debug('parsing Brigade');
            var fc = {
                type: 'FeatureCollection'
            };
            var brigade = brigade.models[0].attributes;

            // Loop through the Geometries, assigning characteristics
            features = _.map(
                ccgGeoms.features,
                function(geometry){
                    var feature = new mapping.CCGFeature();
                    var ccg_code = geometry.ccg_code;
                    feature.properties.ccg_code = ccg_code;
                    feature.geometry = geometry.geometry;

                    var data = brigade[ccg_code] || null;

                    // No prescriptions, no ratio to show
                    if(!data){
                        feature.properties.total_items_month = 0;
                        feature.properties.ccg_problem = 0;
                        return feature;
                    }

                    var tot =  data.group1.items + data.group2.items;
                    feature.properties.total_items_month = tot;
                    feature.properties.ccg_problem = data.group1.proportion;
                    return feature
                }
            );

            fc.features = features;
            return fc;
        },

        // Fetching the Brigade just returned, so now we can add the CCG
        // heatmap features.
        item_added: function(brigade, view){
            log.debug('BucketMap collection got items');
            log.debug(brigade);
            log.debug(view);
            var feature_collection = this.parse_buckets(ccgGeoms, brigade);
            var geoJSON = L.geoJson(
                feature_collection,
                {
                    style: mapping.style,
                    onEachFeature: mapping.onEachFeature
                }
            );
            geoJSON.addTo(this.map);
            mapping.geojson = geoJSON;
        }


    });

    // GET Api calls

    var Api = {

        'product': function(opts){
            pharmacy = new Pharmacy();
            pharmacy.fetch();
            return pharmacy
        },

        'prescriptioncomparison': function(opts){
            brigade = new Brigade();
            brigade.fetch({data: {
                'query_type': opts['query_type'] || 'ccg',
                'group1': opts['group1'].join(','),
                'group2': opts['group2'].join(','),
            }})
            return brigade
        }
    }

    // Api wrapper for producing Map views
    var Maps = {

        bucket: function(opts){
            var comparison = Api.prescriptioncomparison({
                group1:  opts.bucket1 || [],
                group2:  opts.bucket2 || []
            });
            var bucketmap = new BucketMap({
                collection: comparison
            });
            return bucketmap;
        },
    };

    var GET = function(opts){
        log.debug('Getting!');
        log.debug(opts);
        return Api[opts.resource](opts);
    }

    App.get = GET;
    App.maps = Maps;

    // Deal with configuration options passed in to the start method.
    App.addInitializer(function(opts){
        _.extend(App.config, opts);
    });

    // Initialisation API -> api = new Scrip();
    var Scrip = context[namespace] = function(opts){
        App.start(opts);
        return App
    }


})(this.window||exports, "Scrip")









