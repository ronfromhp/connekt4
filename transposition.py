import json 
class Transposition:    

	def __init__(self) :
		try:
			self.ttable = json.load(open("ttable.json", "r"))
		except:
			self.ttable = {}
	def put(self, key , value):
		self.ttable.update({key:value})

	def get(self, key):
		return self.ttable.get(key)
	def reset(self):
		json.dump(self.ttable, open("ttable.json", "w"))
		self.ttable = {}