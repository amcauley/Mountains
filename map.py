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

	def draw(self, filename):
		'''draw the entire map - output to file'''
	
		self.preDrawMtnReport()
	
		f = open(filename,'w')
	
		if(PARAM_DEBUG_EN):
			print("Printing map to "+filename)
	
		f.write('Map seed: ')
		f.write(self.seed)
		f.write('\n'+'-'*(self.nx*self.tiles[0][0].tDim*PARAM_MTN_PRINT_WIDTH+2)+'\n')
	
		for tileY in range(0,self.ny):
			for y in range(tileY*self.tiles[0][0].tDim,tileY*self.tiles[0][0].tDim+self.tiles[0][0].tDim):
				f.write('|')	
				for tileX in range(0,self.nx):

					if(PARAM_DEBUG_EN):
						print("printing row "+str(y)+" of tile ("+str(tileX)+","+str(tileY)+")")
				
					drawMtns = []
					if(tileX in self.mtnsPerTile):
						if(tileY in self.mtnsPerTile[tileX]):
							drawMtns = self.mtnsPerTile[tileX][tileY]
				
					for x in range(tileX*self.tiles[0][0].tDim,tileX*self.tiles[0][0].tDim+self.tiles[0][0].tDim):
					
						altTot = 0
						for m in drawMtns:				
							altPk = m.h - abs(x-m.x) - abs(y-m.y)
							if(altPk > 0):
								altTot += altPk
								
						altStr = " "*PARAM_MTN_PRINT_WIDTH
						if(altTot > 0):
							altStr = str(altTot)
							if(len(altStr) < PARAM_MTN_PRINT_WIDTH):
								altStr = " "*(PARAM_MTN_PRINT_WIDTH-len(altStr))+altStr[-len(altStr):]
							elif(len(altStr) > PARAM_MTN_PRINT_WIDTH):
								altStr = altStr[-PARAM_MTN_PRINT_WIDTH:]
						f.write(altStr)
				f.write('|\n')		
		
		f.write('-'*(self.nx*self.tiles[0][0].tDim*PARAM_MTN_PRINT_WIDTH+2))
		f.close()
	
	
	
	