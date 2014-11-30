'''A collection of "constants"/parameters'''

PARAM_DEBUG_EN_GENERAL      = 0         #general debugging, not specific to mtns, rivers, etc.
PARAM_DEBUG_EN_ZONES        = 0         #zoning info
PARAM_DEBUG_EN_RIVERS       = 0         #enable river debug messages
PARAM_DEBUG_EN_MTNS         = 0         #enable mtn debug messages
PARAM_DEBUG_EN_BEACHES      = 0         #enable beach debugging

PARAM_MAP_SEED              = '94'       #map seed, should be a string less than or equal to 10 chars

PARAM_MAP_SIZE_X            = 30         #number of x tiles in the map
PARAM_MAP_SIZE_Y            = 20         #number of y tiles in the map

PARAM_TILE_SIZE             = 10        #tile size - note that tile randomization might not work as expected yet with other values

PARAM_MAP_PRINT_WIDTH       = 3         #number of characters used to print out map symbols and altitudes

PARAM_MTN_MAX_HEIGHT        = 20        #maximum height of any individual mountain
PARAM_MTN_SLOPE_RAND_SCALE  = .25       #maximum deviation from slope PARAM_MTN_MAX_SLOPE. This makes bounding extend of mountains easier.
PARAM_MTN_MAX_SLOPE         = 1.0       #maximum slope. All actual slopes <= to this. Having a fixed max slope makes bounding mtns easier.

PARAM_MAX_SEED_VAL          = 2**32-1   #random seeds are in the range [0,PARAM_MAX_SEED_VAL]

PARAM_MIN_RIVER_ORIGIN_ALT  = 2
PARAM_RIVER_DEATH_PROB      = .00       #probability of river dying while extending to next y coord