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

})(this.window||exports, "Explore")
