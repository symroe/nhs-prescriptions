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
                '/static/js/data/bnftree.json',
                function(data){
                    Scrip.bnftree = data;
                }
            )
            return true;
        }
    }


})(this.window||exports, "Scrip")
