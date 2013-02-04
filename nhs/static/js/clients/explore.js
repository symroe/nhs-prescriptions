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
            bucket1: '#bucket1',
            bucket2: '#bucket2'
        },

        events: {
            'click button': 'resultise'
        },

        resultise: function(){
            var bucket1 = jQuery('#bucket1 select').attr('value')
            var bucket2 = jQuery('#bucket2 select').attr('value')
            log.debug('make api heatmap call')
            // What we want here is for prescribing.js to
            // return us a view with a heatmap in it.
        }

    })

    var DrugOptionView = Backbone.Marionette.ItemView.extend({
        template: '#drug-option-template',
        tagName: 'option',
        onRender: function(){
            this.$el.attr('value', this.model.get('bnf_code'));
            return
        }
    });

    var DrugSelectView = Backbone.Marionette.CollectionView.extend({
        itemView: DrugOptionView,
        tagName: 'select'
    });

    var ExApp = context[namespace] = new Backbone.Marionette.Application();
    var OP = new Scrip({
            api_host: window.location.host
        })


    ExApp.addRegions({
        container: '#explore-container'
    });

    ExApp.addInitializer(function(options){
        var layout = new ExLayout();
        ExApp.container.show(layout);
        controls = new ExControlLayout()

        all_drugs = OP.get({
            resource: 'product'
        })

        bucket1 = new DrugSelectView({
            collection: all_drugs
        });

        bucket2 = new DrugSelectView({
            collection: all_drugs
        })

        layout.controls.show(controls);
        controls.bucket1.show(bucket1);
        controls.bucket2.show(bucket2);
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
