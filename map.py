import random
from params import *
import tile

class Map:
	'''The map class manages sets of tiles as the top level class '''
	def __init__(self, nx, ny, seed = None):
		self.nx = nx #number of tiles in x dimension
		self.ny = ny #number of tiles in y dimension
		
		#tile (x,y) will be indexed as self.tiles[x][y]
		self.tiles = []
		
		if(seed == None):
			self.seed = str(random.randint(0,PARAM_MAX_SEED_VAL))
		else:
			self.seed = seed
		
		for x in range(0,nx):
			self.tiles.append([])
			for y in range(0,ny):
				random.seed(int(self.seed)+nx*y+x)
				self.tiles[x].append(tile.Tile(x,y,str(random.randint(0,PARAM_MAX_SEED_VAL))))
				
	def preDrawMtnReport(self):
		'''Iterate through tiles and generate any pre-draw info needed, mainly a collection of
		mtns that need to be exported to other tiles (due to extending into their region)'''
		self.mtnsPerTile = {}
		tilemtnsPerTile = {}
		
		for y in range(0,self.ny):
			for x in range(0,self.nx):
				tilemtnsPerTile = self.tiles[x][y].preDrawMtnReport()
				for tileX in tilemtnsPerTile:
					if(tileX not in self.mtnsPerTile):
						self.mtnsPerTile[tileX] = {}
					for tileY in tilemtnsPerTile[tileX]:
						if(tileY not in self.mtnsPerTile[tileX]):
								self.mtnsPerTile[tileX][tileY] = []
						self.mtnsPerTile[tileX][tileY].extend(tilemtnsPerTile[tileX][tileY])
						
						if(PARAM_DEBUG_EN):
							for mtnReport in tilemtnsPerTile[tileX][tileY]:
								print("Adding MtnReport to Map tile ("+str(tileX)+","+str(tileY)+"): peak ("+\
										str(mtnReport.x)+","+str(mtnReport.y)+","+str(mtnReport.h)+")") 					