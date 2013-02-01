void function pendantInit(context){
	var pendants = {};

	// Accessor method
	function getPendant(key){
		return key && pendants[key]
			? pendants[key]
			: pendants;
	};

	function pendant(setup){
		// Internal variables

		// Internal reference
		var pendant      = this;
		var setup        = setup            || {};
		var key          = setup.key        && (function addPendant(){
			pendants[setup.key] = pendant;
		}())                                || void(0);
		var delay        = setup.delay      || 0;
		var patience     = setup.patience   || false;
		// # of dependencies to be resolved
		var dependencies = 0;
		// # of dependencies resolved
		var resolved     = 0;
		// Functions waiting on dependencies 
		var dependants   = setup.dependants || [];
		// Whether this pendant is resolved or not
		var fulfilled    = false;
		// Holds timeout for delayed fullfill function
		var countdown;
		// Store data from dependencies
		var resolution;


		// Exposed functions

		// Pass in function(s) for immediate execution:
		// It registers a dependency and passes reference to a function that resolves it.
		pendant.addDependency = function addDependency(dependency){
			if(!dependency)
				return pendant;

			if(countdown)
				clearTimeout(countdown);

			// Accepts multiple functions in array form or separate arguments.
			var newDependencies = 
				Object.prototype.toString.call(dependency) == '[object Array]' 
				? arguments[0] 
				: arguments;

			for(var i = 0, l = newDependencies.length; i < l; ++i){
				++dependencies;

				// Dependencies are executed immediately and passed a new resolution,
				// Which exposes a resolve function to be called as an when desired.
				newDependencies[i](makeResolution(), pendant);
			}

			return pendant;
		};

		// Pass in a function that gets called when all dependencies have been resolved,
		// or executes immediately if resolution has been fulfilled.
		pendant.addDependant = function addDependant(dependant){
			if(fulfilled && !patience){
				dependant(pendant);
			}
			else {
				dependants.push(dependant);
			}

			return pendant;
		};

		// Turn fulfillment on or off, useful for pausing til arbitrary points
		pendant.off          = function pendantOff(){
			pendant.patience = true;
			
			return pendant;
		};

		pendant.on           = function pendantOn(){
			pendant.patience = false;

			if(dependencies == resolved){
				attemptFulfillment();
			}

			return pendant;
		};
		// Getters
		pendant.info         = function getInfo(){
			return {
				dependants   : dependants,
				dependencies : dependencies,
				fulfilled    : fulfilled,
				key          : key,
				patience     : patience,
				resolved     : resolved,
				resolution   : resolution
			}
		};
		pendant.dependants   = function getDependants(){
			return dependants
		};
		pendant.dependencies = function getDependencies(){
			return dependencies
		};
		pendant.fulfilled    = function getFulfilled(){
			return fulfilled
		};
		pendant.key          = function getKey(){
			return key
		};
		pendant.patience     = function getPatience(){
			return patience
		};
		pendant.resolved     = function getResolved(){
			return resolved
		};
		pendant.resolution   = function getResolution(){
			return resolution
		};

		// Internal functions

		// Initialise any passed-in dependencies
		setup.dependencies && void function init(){
			pendant.addDependency(setup.dependencies);
		}();

		function makeResolution(){
			// Internal state to prevent multiple resolutions of same dependency
			var dependencyResolved = false;
			// Placeholder
			var index              = resolutions.length;

			// Exposed to dependency functions 
			return function resolve(data){
				if(!dependencyResolved){
					++resolved;

					if(data)
						resolution = data;

					dependencyResolved = true;

					if(resolved >= dependencies){
						attemptFulfillment();
					}
				}

				// Return pendant to calling dependency function, 
				// Allows state-checking, further manipulation, etc
				return pendant;
			}
		}

		function attemptFulfillment(){
			if(patience){
				return;
			}

			countdown = setTimeout(function fulfill(){
				fulfilled = true;

				while(dependants.length){
					// Dependants are shifted out then executed.
					// Pendant can then be seen to have 0 dependants.
					dependants.shift()(pendant);
				}

				// Clear reference
				countdown = void 0;
			}, delay);
		}

		return this;
	};

	context.Pendant     = function pendantAccessor(x){
		return new pendant(x);
	};

	context.Pendant.get = getPendant;
}(this);
