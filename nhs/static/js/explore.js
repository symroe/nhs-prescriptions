//
// explore.js
//
//
// Explore
//
//
// Naming conventions is file:
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
// Explore _ $ Backbone Mustache
//

// Code:
(function(context, namespace){


    function definedp(that){
        return typeof that !='undefined';
    }

    //
    // Let's sort out our dependencies
    //
    if (typeof $ === 'undefined'&& (typeof require !== 'undefined')){
        $ = require('jquery');
    }
    if (typeof _ === 'undefined'&& (typeof require !== 'undefined')){
        _ = require('underscore');
    }
    if (typeof Backbone === 'undefined'&& (typeof require !== 'undefined')){
        Backbone = require('backbone');
    }

    if(typeof process !== 'undefined' && typeof process.argv !== 'undefined' && typeof require !== 'undefined'){
        _debuglog = function(x){
            if(_.indexOf(process.argv, 'explore/test/js') != -1){
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

    //
    // #js has quite an ugly API for many common operations.
    // Extend the basic operations for utility
    //
    String.prototype.capitalize = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
    }

    //
    // Private closured helpers
    //
    var tpltext = function(identifier){
        return $(identifier).text()
    };


    //
    // Unexplore an object into a list of objects where
    // each object has a .key and a .value that are
    // equivalent to the original object's key/value pairs
    //
    var unexplore = function(obj){
        var unexploreped = []
        for (var prop in obj){
            if (obj.hasOwnProperty(prop)){
                unexploreped.push({
                    'key' : prop,
                    'value' : obj[prop]
                });
            }
        }
        return unexploreped
    }

    // Explore a list of key/val pairs into an object
    var explore = function(lst){
        var exploreped = {};
        _.map(lst, function(item){exploreped[item[0]] = item[1]});
        return exploreped;
    }

    $(document).ready(function(){
        $('#go').click(function(){
            var frist = $("#frist").attr('value')
            var next = $("#next").attr('value')

            log.debug(frist)
            log.debug(next)

            var ccgData = {
                "type": "FeatureCollection",
                "features": _.map(
                    ccgGeoms.features,
                    function(geom){
                        var feat = {
                            type: "Feature",
                            properties: {
                                "ccg_code": geom.ccg_code,
                                "name": geom.ccg_code,
                                "ccg_name": "some name",
                                "total_items_month": 456,
                                "Description": "<div>This is some markup</div>",
                                "ccg_problem": 54.8
                                },
                            "geometry": geom.geometry
                            }
                        return feat
                        }
                    )
            }

            var geojson = L.geoJson(ccgData, { style: style,
			                       onEachFeature: onEachFeature}).addTo(map);


        })
    })

    // layout.render();

    // context.Explore = Explore;1
})(this.window||exports, "Explore")



// var ccgData = {
//   "type" : "FeatureCollection",
//   "features" : [ {
//     "type" : "Feature",
//     "properties" : {
//       "ccg_code" : "07L",
//       "Name" : "07L",
//       "ccg_name" : "NHS Barking &amp; Dagenham CCG",
//       "total_items_month" : 16642,
//       "Description" : "<div class=\"googft-info-window\" style=\"font-family:sans-serif\"> <b>CCG code:</b> 07L<br> <b>CCG name:</b> NHS Barking &amp; Dagenham CCG<br> <b>No. of practices:</b> 42<br> <b>Population:</b> 196400<br> <b>No. of LSOAs:</b> 109<br> <b>Region:</b> London </div>",
//       "ccg_problem" : 21.099999999999998,
//       "pop_per_surgery" : 4676.190476190476,
//       "no_of_practices" : 42,
//       "no_of_lsoas" : 109,
//       "population" : 196400,
//       "region" : "London"
//     },
//     "geometry" : {
//       "type" : "Polygon",
//       "coordinates" : [ [ [ 0.067973, 51.543554 ], [ 0.066708, 51.540982 ], [ 0.069054, 51.537389 ], [ 0.067909, 51.53613 ], [ 0.069759, 51.535996 ], [ 0.072833, 51.529201 ], [ 0.078127, 51.529267 ], [ 0.085262, 51.525838 ], [ 0.092534, 51.525688 ], [ 0.094901, 51.516996 ], [ 0.099821, 51.514429 ], [ 0.09973, 51.511844 ], [ 0.108003, 51.511484 ], [ 0.128831, 51.515477 ], [ 0.157971, 51.508708 ], [ 0.164468, 51.527005 ], [ 0.174455, 51.538032 ], [ 0.179271, 51.540294 ], [ 0.180479, 51.544061 ], [ 0.185809, 51.547165 ], [ 0.190205, 51.552626 ], [ 0.184768, 51.556371 ], [ 0.184734, 51.559903 ], [ 0.182645, 51.561258 ], [ 0.18516, 51.565451 ], [ 0.173413, 51.565045 ], [ 0.161878, 51.561546 ], [ 0.151496, 51.56792 ], [ 0.146784, 51.568716 ], [ 0.149778, 51.569643 ], [ 0.147056, 51.57632 ], [ 0.14747, 51.5807 ], [ 0.150952, 51.583702 ], [ 0.151223, 51.589072 ], [ 0.151057, 51.595475 ], [ 0.149775, 51.597022 ], [ 0.147594, 51.596753 ], [ 0.148162, 51.598996 ], [ 0.146588, 51.599399 ], [ 0.129554, 51.590005 ], [ 0.131039, 51.587454 ], [ 0.126423, 51.586652 ], [ 0.127703, 51.58158 ], [ 0.132589, 51.581261 ], [ 0.133542, 51.579909 ], [ 0.130865, 51.57934 ], [ 0.131681, 51.577029 ], [ 0.129262, 51.576222 ], [ 0.131584, 51.571782 ], [ 0.129875, 51.571544 ], [ 0.129374, 51.566396 ], [ 0.119198, 51.562945 ], [ 0.117503, 51.55911 ], [ 0.120468, 51.558454 ], [ 0.118962, 51.557294 ], [ 0.113353, 51.557264 ], [ 0.114766, 51.55525 ], [ 0.111883, 51.552556 ], [ 0.108447, 51.552627 ], [ 0.093483, 51.545744 ], [ 0.092518, 51.549539 ], [ 0.077946, 51.544045 ], [ 0.067973, 51.543554 ] ] ]
//     }
//   }, {
//     "typ
