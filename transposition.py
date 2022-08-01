class Transposition:

	def __init__(self) :
		self.ttable = {}

	def put(self, key , value):
		self.ttable.update({key:value})

	def get(self, key):
		return self.ttable.get(key)
	def reset(self):
		self.ttable = {}
