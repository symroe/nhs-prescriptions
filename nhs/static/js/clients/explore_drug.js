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
        template: '#explore-drug-controls-template',

        regions: {
            drugs: '#drugs',
        },

        events: {
            'click button': 'resultise',
            'keyup #filter': 'filter'
        },

        // Show the results
        resultise: function(){
            log.debug('Make Heatmap!');
            var bnf_code = jQuery('#drugs select').attr('value');
            var mapview = OP.maps.scrips_per_capita({
                bnf_code: bnf_code
            });
            log.debug(mapview);
            ExploreDrugApp.trigger('results:new_view', mapview);
        },

        // Filter the visible drugs
        filter: function(event){
            log.debug('filtering')
            var val = this.$('#filter').attr('value');
            log.debug(val);
            this.drugs.currentView.filter(val);
        }

    })

    var ExResultLayout = Backbone.Marionette.Layout.extend({
        template: '#explore-results-template',

        regions: {
            results: '#explore-results'
        },

        new_result: function(view){
            log.debug(view);
            this.results.show(view);
        }

    })

    var DrugListItemView = Backbone.Marionette.ItemView.extend({
        template: '#drug-option-template',
        tagName: 'li',
        onRender: function(){
            this.$el.attr('value', this.model.get('bnf_code'));
            return
        }
    });

    var DrugSelectView = Backbone.Marionette.CollectionView.extend({
        itemView: DrugListItemView,
        tagName: 'ul',

        // We'd like to hide any drugs that don't match VAL
        filter: function(val){
            log.debug(val);
            var matches = _(this.collection.search(val)).pluck('cid');
            this.$('li').toggle(false);

            _.each(
                matches, function(x){
                    this.children._views[this.children._indexByModel[x]].$el.toggle(true);
                },
                this);
        }
    });

    var ExploreDrugApp = context[namespace] = new Backbone.Marionette.Application();
    var OP = new Scrip({
            api_host: window.location.host
        })

    ExploreDrugApp.addRegions({
        container: '#explore-container'
    });

    ExploreDrugApp.addInitializer(function(options){
        var layout = new ExLayout();
        ExploreDrugApp.container.show(layout);
        controls = new ExControlLayout();
        results = new ExResultLayout();
        ExploreDrugApp.on('results:new_view', results.new_result, results);

        all_drugs = OP.get({
            resource: 'product',
            data: { limit: 0 }
        })

        drugs = new DrugSelectView({
            collection: all_drugs
        });

        layout.controls.show(controls);
        controls.drugs.show(drugs);
        layout.results.show(results);
    });

})(this.window||exports, "ExploreDrug")
