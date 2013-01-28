//
// scrip.js
//
//
// Prescriptions utilites
//
//
// Naming conventions in this file:
//
// Objects:                /[A-Z][a-z]+([A-Z][a-z]+)?/
// Instantiated objects:   /[a-z][a-z]+([A-Z][a-z]+)?/
// Namespaces:             /[a-z]+/
// Constructors:           /initialize/
// Application:            /[A-Z][A-Z]+/
// Top level constants:    /[A-Z][A-Z]+/
//
// Reserved Names:
//
// Scrip _ $ Backbone Mustache
//

// Code:
(function(context, namespace){



    if(typeof process !== 'undefined' && typeof process.argv !== 'undefined' && typeof require !== 'undefined'){
        _debuglog = function(x){
            if(_.indexOf(process.argv, 'zip/test/js') != -1){
                return;
            }
            console.log('indebuglog')
            console.log(process.argv)
            return
        }
    }else{
        _debuglog = function(x){
            console.log(x)
        }
    }

    var log = {
        debug: _debuglog
    }

    var Scrip = context[namespace] = {
        get_bnf: function(){
            $.getJSON(
                '/static/js/data/bnfmarion.json',
                function(data){
                    Scrip.bnftree = data;
                }
            )
            return true;
        },

        practice: {},
        ccg: {}

    }

    Scrip.ccg.bucket_compare = function(options){
        var naughty, nice = options.naughty, options.nice;
        var map = options.map

        $.ajax(
            '/api/v1/prescriptioncomparison/',
            {
                data: {
                    format: 'json',
                    group1: naughty.join(),
                    group2: nice.join(),
                    query_type: 'ccg'
                },
                success: function(data){

                    var features = _.map(
                        ccgGeoms.features,
                        function(geom){

                            var scrips = data[geom.ccg_code]

                            var feat = {
                                type: "Feature",
                                properties: {
                                    "ccg_code": geom.ccg_code,
                                    "name": geom.ccg_code,
                                    "ccg_name": "some name",
                                    "total_items_month": scrips.group1.items+scrips.group2.items,
                                    "Description": "<div>This is some markup</div>",
                                    "ccg_problem": scrips.group1.proportion
                                },
                                "geometry": geom.geometry
                            }
                            return feat
                        }
                    )

                    var ccgData = {
                        "type": "FeatureCollection",
                        "features": features
                    }

                    var geojson = L.geoJson(
                        ccgData, { style: style,
			           onEachFeature: onEachFeature}).addTo(map);

                }
            }
        )
    }

    Scrip.practice.bucket_compare = function(options){
        var naughty, nice = options.naughty, options.nice;
        var map = options.map

        $.ajax(
            '/api/v1/some/field/',
            {
                data: {},
                success: function(bucketdata){

                    $.ajax(
                        '/api/v1/practice',
                        {
                            data: {
                                'format': 'json',
                                'limit': 0
                            },
                            success: function(practicedata){
                                var markers = new L.MarkerClusterGroup({disableClusterAtZoom: 14});

                                _.each(practicedata, function(practice){
                                    var marker1 = L.marker([practice.location.lat, practice.location.lng]);
                                     = bucketata
                                    marker1.bindPopup()
                                    markers.addLayer(marker1)

                                })

                                var practiceScrips = _.pairs(data);
//http://localhost:4567/api/v1/practice/?format=json&limit=0

                            }



                }
            }
        )

    }


})(this.window||exports, "Scrip")
