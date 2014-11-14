import random
from params import *
import mtn

class Rivers:
	'''The rivers class describes the flowing water within the tile'''
	
	tDim = PARAM_TILE_SIZE #river size - MUST MATCH TILE CLASS SIZE
	
	def __init__(self, cornerXY, seed = None):
		'''inputs:	cornerXY	= (X,Y) pair of top left corner bounding this river set
					seed		= usual random seed param for a class '''
		
		self.x = cornerXY[0]
		self.y = cornerXY[1]
		self.entryPtsXY = []
		self.mtns = []
		
		if(seed == None):
			self.seed = str(random.randint(0,PARAM_MAX_SEED_VAL))
		else:
			self.seed = seed
			
		'''use the seed to generate any new rivers'''
		self.originPts = []
		for newRiver in range(0,int(self.seed[0])%2):
			rx = self.x + int(self.seed[-1])%self.tDim
			ry = self.y + int(self.seed[-2])%self.tDim
			self.originPts.extend((rx,ry))	
		
		self.xyPts = {}
		self.exitPts = {}
		
	def preDrawRiverReport(self, entryPtsXY, mtns):
		'''generate the list of river x,y coords (global units) in this river tile
					entryPtsXY	= list of (X,Y) river entry points in global coords
					mtns		= list of mtns that can influence this river set / tile '''
		
		self.entryPtsXY = entryPtsXY
		self.mtns = mtns
		
		'''combine all beginnings of rivers within this river tile'''
		startPts = self.originPts.extend(self.entryPtsXY)
		
		'''form the river paths one at a time'''
		for startPt in startPts:
			rx = startPt[0]
			ry = startPt[1]
			'''build the path until we exit the river tile or it dies naturally'''
			while(True):
				#TODO: Add river elevation calc, can probably just copy from tile draw routine
				thisAlt = 0
				ry += 1
				if (ry >= self.y + self.tDim):
					'''river continues into the next river tile'''
					exitX = rx+random.randint(-1,1)
					if (exitX not in self.exitPts):
						self.exitPts[exitX] = []
					self.exitPts[exitX].extend(ry)
					continue
				
				goodNextX = []
				for nextX in range(rx-1,rx+2):
					if (nextX < self.x or nextX >= self.x+self.tDim):
						continue
					#TODO: Add river elevation check for new x,y, can probably just copy from tile draw routine
					nextAlt = 0
					if(nextAlt > thisAlt):
						continue
					'''random death'''
					if(random.random < PARAM_RIVER_DEATH_PROB):
						continue
					goodNextX.extend(nextX)
				
				rx = random.choice(goodNextX)
				if (rx not in self.xyPts):
					self.xyPts[rx] = []
				self.xyPts[rx].extend(ry)
			
				
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		