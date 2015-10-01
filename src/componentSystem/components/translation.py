
from pyrr import matrix44, vector3

class TranslationComponent(object):

	def __init__(self, entityName, componentInfo):
		self.x = componentInfo["x"]
		self.y = componentInfo["y"]
		self.rot = componentInfo.get("rot", 0)
		self.dirty = False
		self._matrix = None
		self.CalculateMatrix()

	def CalculateMatrix(self):
		self._matrix = matrix44.create_from_translation(vector3.create(self.x, self.y, 0.0))
		self.dirty = False

	def SetPosition(self, x, y):
		self.x = x
		self.y = y
		self.dirty = True

	def SetRotation(self, rot):
		self.rot = rot
		self.dirty = True

	def GetAsMatrix(self):
		if self.dirty:
			self.CalculateMatrix()
		return self._matrix

	matrix = property(GetAsMatrix)