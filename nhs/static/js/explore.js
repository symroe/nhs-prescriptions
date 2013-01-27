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

    var Explore = new Backbone.Marionette.Application();

    BnfTreeWidget = Backbone.Marionette.Layout.extend({
        template: "#bnftree-template",

        regions: {
            title: "#title",
            tree: "#tree"
        },

        initialize: function(el, collection){
            this.el = el;
            this.collection = collection;
        },

        render: function(){

            var items = _.map(this.collection.models, function(model){
                bnf = new BnfItemView({model: model})
                return bnf.render()
            })
            var $el = this.$el;
            var that = this
            this.el.slideUp(function(){
                that.el.html('')
                _.each(items, function(item){
                    $el.append(item.el)
                });
                that.el.append($el[0]);
                that.el.slideDown()
            })
        }

    });

    BnfItemView = Backbone.View.extend({

        events: {
            'click': 'dive'
        },

        initialize: function(opts){
            this.model = opts.model;
        },

        render: function(){
            this.$el.html(this.model.attributes.nodeName)
            return this;
        },

        dive: function(){
            log.debug(this.model.attributes.nodeName);
            if(this.model.nodes){
                var bnf_tree = this.model.nodes;
                Explore.bnftree_widget = new BnfTreeWidget($('#bnf-tree'), bnf_tree);
                Explore.bnftree_widget.render()
            }else{
                log.debug('bottom!'+ this.model.attributes.nodeName)
                log.debug(this.model.attributes.bnfPart)
            }
        }

    })


    BnfTreeView = Backbone.Marionette.CompositeView.extend({
        template: "#bnf-node-template",

        tagName: "ul",

        initialize: function(){
            this.collection = this.model.nodes;
        },

        appendHtml: function(collectionView, itemView){
            collectionView.$("li:first").append(itemView.el);
        }
    });

    var BnfTreeRoot = Backbone.Marionette.CollectionView.extend({
        itemView: BnfTreeView
    });


    BnfTreeNode = Backbone.Model.extend({
        initialize: function(){
            var nodes = this.get("nodes");
            if (nodes){
                this.nodes = new BnfTreeNodeCollection(nodes);
                this.unset("nodes");
            }
        }
    });

    var BnfTreeNodeCollection = Backbone.Collection.extend({
        model: BnfTreeNode
    });


    Explore.addInitializer(function(){

        // Render the layout and get it on the screen, first

        $.getJSON(
            '/static/js/data/bnfmarion.json',
            function(bnfData){

                var bnf_tree = new BnfTreeNodeCollection(bnfData)

                Explore.bnftree_widget = new BnfTreeWidget($('#bnf-tree'), bnf_tree);

                var layoutRender = Explore.bnftree_widget.render()


                // var bnfTreeView = new BnfTreeRoot({
                //     collection: bnf_tree
                // })

                // bnfTreeView.render()
                // $("#backbone-main").append(bnfTreeView.el);

                // This kicks off the rest of the app, through the router
                Backbone.history.start();

            }
        );

    });

    Explore.start()

    // layout.render();

    context.Explore = Explore;
})(this.window||exports, "Explore")
