import random
import math
from params import *

class Mtn:
	'''Mountain class. x and y are global, not relative to tile'''
	def __init__(self, x, y, h, seed = None):
		self.x = x
		self.y = y
		self.h = h
		
		if(seed == None):
			self.seed = str(random.randint(0,PARAM_MAX_SEED_VAL))
		else:
			self.seed = seed
			
	def altAtXY(self, x, y):
		'''return the altitude of this mountain at coord x,y'''
		#square based mtns:
		#return self.h - abs(x-self.x) - abs(y-self.y)
		
		#rounded mtns:
		return int(self.h - math.sqrt((x-self.x)**2 + (y-self.y)**2))