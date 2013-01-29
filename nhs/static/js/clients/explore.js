//
// explore.js

(function(context, namespace){

    // Setup logging
    if(typeof process !== 'undefined' && typeof process.argv !== 'undefined' && typeof require !== 'undefined'){
        _debuglog = function(x){
            if(_.indexOf(process.argv, 'explore/test/js') != -1){
                return;
            }
        }
    }else{
        _debuglog = function(x){
            console.log(x)
        }
    }

    var log = {
        debug: _debuglog
    }

    var ExLayout = Backbone.Marionette.Layout.extend({
        template: '#explore-layout-template',

        regions: {
            controls: '#explore-controls',
            results: '#explore-results'
        }
    });

    var ExControlLayout = Backbone.Marionette.Layout.extend({
        template: '#explore-controls-template',

        regions: {
            bucket: '#bucket1',
            bucket2: '#bucket2'
        }
    })

    var DrugOptionView = Backbone.Marionette.ItemView.extend({
        template: '#drug-option-template'
    });

    var DrugSelectView = Backbone.Marionette.CollectionView.extend({
        itemView: DrugOptionView
    });

    var ExApp = context[namespace] = new Backbone.Marionette.Application();

    ExApp.addRegions({
        container: '#explore-container'
    });

    ExApp.addInitializer(function(options){
        var layout = new ExLayout();
        ExApp.container.show(layout);
        controls = new ExControlLayout()

        OP = new Scrip({
            api_host: window.location.host
        })

        all_drugs = OP.get({
            resource: 'product'
        })

        bucket1 = new DrugSelectView({
            collection: all_drugs
        })

        controls.bucket.show(bucket1);

        layout.controls.show(controls);
    });

})(this.window||exports, "Explore")



    // $(document).ready(function(){
    //     $('#go').click(function(){
    //         var frist = $("#frist").attr('value')
    //         var next = $("#next").attr('value')

    //         log.debug(frist)
    //         log.debug(next)

    //         var ccgData = {
    //             "type": "FeatureCollection",
    //             "features": _.map(
    //                 ccgGeoms.features,
    //                 function(geom){
    //                     var feat = {
    //                         type: "Feature",
    //                         properties: {
    //                             "ccg_code": geom.ccg_code,
    //                             "name": geom.ccg_code,
    //                             "ccg_name": "some name",
    //                             "total_items_month": 456,
    //                             "Description": "<div>This is some markup</div>",
    //                             "ccg_problem": 54.8
    //                             },
    //                         "geometry": geom.geometry
    //                         }
    //                     return feat
    //                     }
    //                 )
    //         }

    //         var geojson = L.geoJson(ccgData, { style: style,
    //                                            onEachFeature: onEachFeature}).addTo(map);


    //     })
    // })
