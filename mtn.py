import random
from params import *

class Mtn:
	'''Mountain class'''
	def __init__(self, x, y, h, seed = None):
		self.x = x
		self.y = y
		self.h = h
		
		if(seed == None):
			self.seed = str(random.randint(0,PARAM_MAX_SEED_VAL))
		else:
			self.seed = seed