import random
from params import *
import mtn

class Tile:
	'''Tile class to combine mountains, rivers, etc.'''
	
	tDim = PARAM_TILE_SIZE #size of tiles is a property of the class
	
	def __init__(self, x, y, seed = None):
		self.mtnList = [];
		
		self.x = x
		self.y = y
		self.minH = 0
		self.maxH = 10
		
		if(seed == None):
			self.seed = str(random.randint(0,PARAM_MAX_SEED_VAL))
		else:
			self.seed = seed
			
		'''if necessary, pad seed to full 10 digits'''
		self.seed = '0'*(10-len(self.seed)) + self.seed
		
		if(PARAM_DEBUG_EN):
			print("tile init, x y seed: "+str(x)+" "+str(y)+" "+str(self.seed))
		
		xyTuples = []
		for m in range(0,int(self.seed[-10])%3):
			mx = int(self.seed[-3*m-3])
			my = int(self.seed[-3*m-2])
			mh = int(self.seed[-3*m-1])
			
			'''skip duplicate x,y peak locations'''
			if((mx,my) in xyTuples):
				continue

			self.mtnList.append(mtn.Mtn(mx, my,	mh,	str(random.randint(0,PARAM_MAX_SEED_VAL))))
		
	def point2TileDist2(self, thisX, thisY, tileX, tileY):
		''' compute distance squared between this tile's (x,y) and the closest point
		on tile (tileX, tileY) '''
		
		absX = self.x*self.tDim + thisX
		absY = self.y*self.tDim + thisY
		
		#TODO: Replace hard-coded tile/map size with a constant
		xDist2 = 0
		if(self.x > tileX):
			xDist2 = (absX - (tileX*self.tDim+self.tDim-1))**2
		elif(self.x < tileX):
			xDist2 = (absX - tileX*self.tDim)**2	
		
		yDist2 = 0
		if(self.y > tileY):
			yDist2 = (absY - (tileY*self.tDim+self.tDim-1))**2
		elif(self.y < tileY):
			yDist2 = (absY - tileY*self.tDim)**2	
			
		if(PARAM_DEBUG_EN):
			print("("+str(absX)+","+str(absY)+") dist2 to tile ("+str(tileX)+","+str(tileY)+") = "+str(xDist2+yDist2))	
			
		return xDist2 + yDist2
		
	def preDrawMtnReport(self):
		'''Report which tiles the mtns in this tile extend into (including this tile itself)'''
		mtnExport = {}
		for m in range(0,len(self.mtnList)):
			cenX = self.mtnList[m].x
			cenY = self.mtnList[m].y
			radius = self.mtnList[m].h
			
			#TODO: Replace hard-coded tile/map size with a constant
			for tileX in range(int((self.x*self.tDim+cenX-radius)/self.tDim), int((self.x*self.tDim+cenX+radius)/self.tDim+1)):
				for tileY in range(int((self.y*self.tDim+cenY-radius)/self.tDim), int((self.y*self.tDim+cenY+radius)/self.tDim+1)):
					if(tileX >= 0 and tileX < self.tDim and tileY >= 0 and tileY < self.tDim):
						if(self.point2TileDist2(cenX, cenY, tileX, tileY) < radius**2):
							if((tileX) not in mtnExport):
								mtnExport[tileX] = {}
							if((tileY) not in mtnExport[tileX]):
								mtnExport[tileX][tileY] = []
							mtnExport[tileX][tileY].append(mtn.Mtn((self.x*self.tDim+cenX), (self.y*self.tDim+cenY), radius))
							
							if(PARAM_DEBUG_EN):
								print("Adding Mtn to tile ("+str(tileX)+","+str(tileY)+"): peak ("+\
										str(self.x*self.tDim+cenX)+","+str(self.y*self.tDim+cenY)+","+str(radius)+")") 
		return mtnExport
									
		
	def draw(self, drawMtns):
		'''Currently "drawing" the tile just means print it out in glorious ASCII'''
	
		if(PARAM_DEBUG_EN):
			print("Tile ("+str(self.x)+","+str(self.y)+"), seed "+str(self.seed))
		
		for y in range(self.y*self.tDim,self.y*self.tDim+self.tDim):
			for x in range(self.x*self.tDim,self.x*self.tDim+self.tDim):
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
				print(altStr, end="")
				
			print("\n")
					