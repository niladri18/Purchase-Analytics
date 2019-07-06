import os
import sys
import pdb

class Product:
	def __init__(self, data):
		self.name = ""
		self.dept =  int(data[-1])
		self.aisl =  int(data[-2])
		for i in range(1,len(data)-2):
			self.name += data[i] + ","
		self.name = self.name[:-1]
		# Set the default number of orders to zero 
		self.order = 0
		pass

	def addOrder(self):
		self.order += 1
		pass

	def getOrder(self):
		return self.order

