'''A collection of "constants"/parameters'''

PARAM_DEBUG_EN			= 0 		#enable debug messages

PARAM_MAP_SEED			= '4'		#map seed, should be a string less than or equal to 10 chars

PARAM_MAP_SIZE_X		= 10			#number of x tiles in the map
PARAM_MAP_SIZE_Y		= 10			#number of y tiles in the map

PARAM_TILE_SIZE 		= 10		#tile size - note that tile randomization might not work as expected yet with other values
PARAM_MTN_PRINT_WIDTH 	= 3			#number of characters used to print out mtn altitudes
PARAM_MAX_SEED_VAL 		= 2**32-1	#random seeds are in the range [0,PARAM_MAX_SEED_VAL]

PARAM_RIVER_DEATH_PROB	= .05		#probability of river dying while extending to next y coord