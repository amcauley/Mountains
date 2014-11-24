'''A collection of "constants"/parameters'''

PARAM_DEBUG_EN_GENERAL      = 0         #general debugging, not specific to mtns, rivers, etc.
PARAM_DEBUG_EN_RIVERS       = 0         #enable river debug messages
PARAM_DEBUG_EN_MTNS         = 0         #enable mtn debug messages

PARAM_MAP_SEED              = '3'       #map seed, should be a string less than or equal to 10 chars

PARAM_MAP_SIZE_X            = 64         #number of x tiles in the map
PARAM_MAP_SIZE_Y            = 48         #number of y tiles in the map

PARAM_TILE_SIZE             = 10        #tile size - note that tile randomization might not work as expected yet with other values

PARAM_MAP_PRINT_WIDTH       = 3         #number of characters used to print out map symbols and altitudes

PARAM_MTN_MAX_HEIGHT        = 10        #maximum height of any individual mountain

PARAM_MAX_SEED_VAL          = 2**32-1   #random seeds are in the range [0,PARAM_MAX_SEED_VAL]

PARAM_MIN_RIVER_ORIGIN_ALT  = 2
PARAM_RIVER_DEATH_PROB      = .00       #probability of river dying while extending to next y coord