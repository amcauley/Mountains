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
		for r in range(0,int(self.seed[0])%3):
			rx = self.x + int(self.seed[-2*r-1])%self.tDim
			ry = self.y + int(self.seed[-2*r-2])%self.tDim
			self.originPts.append((rx,ry))	
		
		self.xyPts = {}
		self.exitPts = {}
		
		if(PARAM_DEBUG_EN_ALL or PARAM_DEBUG_EN_RIVERS):
			print("New River, ((x,y), seed, originPts) = ("+str((self.x,self.y))+", "+str(self.seed)+", "+str(self.originPts)+")")
		
	def preDrawRiverReport(self, entryPtsXY, mtns):
		'''generate the list of river x,y coords (global units) in this river tile
					entryPtsXY	= list of (X,Y) river entry points in global coords
					mtns		= list of mtns that can influence this river set / tile '''
		
		self.xyPts = {}
		self.exitPts = {}
		
		self.entryPtsXY = entryPtsXY
		self.mtns = mtns
		
		
		'''combine all beginnings of rivers within this river tile'''
		startPts = entryPtsXY
		
		for o in self.originPts:
			alt = 0
			for m in mtns:				
				altPk = m.altAtXY(o[0],o[1])
				if(altPk > 0):
						alt += altPk
			if (alt >= PARAM_MIN_RIVER_ORIGIN_ALT):
				startPts.append(o)
		
		if(PARAM_DEBUG_EN_ALL or PARAM_DEBUG_EN_RIVERS):
			print("river originPts: "+str(self.originPts)+", entryPtsXY: "+str(entryPtsXY)+" mtns: "+str(mtns))		
		
		'''form the river paths one at a time'''
		for startPt in startPts:
			rx = startPt[0]
			ry = startPt[1]
			
			'''write the origin point then start looking for next points'''
			if (rx not in self.xyPts):
				self.xyPts[rx] = []
			self.xyPts[rx].append(ry)
				
			'''build the path until we exit the river tile or it dies naturally'''
			while(True):
				'''river elevation calc'''
				thisAlt = 0
				for m in mtns:				
					altPk = m.altAtXY(rx,ry)
					if(altPk > 0):
						thisAlt += altPk
				
				ry += 1
				if (ry >= self.y + self.tDim):
					'''river continues into the next river tile'''
					exitX = rx+random.randint(-1,1)
					if (exitX not in self.exitPts):
						self.exitPts[exitX] = []
					self.exitPts[exitX].append(ry)
					break
				
				goodNextX = []
				for nextX in range(rx-1,rx+2):
					if (nextX < self.x or nextX >= self.x+self.tDim):
						continue
						
					'''river elevation check for new x,y'''
					nextAlt = 0
					for m in mtns:				
						altPk = m.altAtXY(nextX,ry)
						if(altPk > 0):
							nextAlt += altPk
					
					if(nextAlt > thisAlt):
						continue
						
					goodNextX.append(nextX)
						
				if(PARAM_DEBUG_EN_ALL or PARAM_DEBUG_EN_RIVERS):		
					print("river current (x,y) = ("+str(rx)+","+str(ry-1)+"), goodNextX = "+str(goodNextX)) 
					
				'''random death'''
				if(random.random() < PARAM_RIVER_DEATH_PROB):
					if(PARAM_DEBUG_EN_ALL or PARAM_DEBUG_EN_RIVERS):	
						print("river death")
					break
				if(not goodNextX):
					break
					
				rx = random.choice(goodNextX)
				if (rx not in self.xyPts):
					self.xyPts[rx] = []
				self.xyPts[rx].append(ry)
			
		if(PARAM_DEBUG_EN_ALL or PARAM_DEBUG_EN_RIVERS):
			print("river xyPts: "+str(self.xyPts)+" exitPts: "+str(self.exitPts))
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		