
from pyrr import matrix44, vector3

class TranslationComponent(object):

	def __init__(self, entityName, componentInfo):
		self.x = componentInfo["x"]
		self.y = componentInfo["y"]
		self.rot = componentInfo.get("rot", 0)
		self.scale = (1.0, 1.0, 1.0)
		self.dirty = False
		self._matrix = None
		self.CalculateMatrix()

	def CalculateMatrix(self):
		translation = matrix44.create_from_translation(vector3.create(self.x, self.y, 0.0))
		rotation = matrix44.create_from_z_rotation(self.rot)
		scale = matrix44.create_from_scale(self.scale)

		self._matrix = matrix44.multiply( matrix44.multiply(scale, rotation), translation)
		self.dirty = False

	def SetPosition(self, x, y):
		self.x = x
		self.y = y
		self.dirty = True

	def SetRotation(self, rot):
		self.rot = rot
		self.dirty = True

	def SetScale(self, scaleX, scaleY):
		self.scale = (scaleX, scaleY, 1.0)
		self.dirty = True

	def GetAsMatrix(self):
		if self.dirty:
			self.CalculateMatrix()
		return self._matrix

	matrix = property(GetAsMatrix)