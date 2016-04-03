from pyrr import matrix44, vector3, quaternion
from componentSystem.components.component import Component

class TransformComponent(Component):
	__requiredAttributes__ = ["pos", "rotAngle"]
	"""
		Defines a Transform component
	"""

	def __init__(self, entityName, componentInfo):
		Component.__init__(self, entityName, componentInfo)
		self.position = vector3.create(self.pos[0], self.pos[1], self.pos[2])
		self.rotation = quaternion.create_from_z_rotation(self.rotAngle)
		self.worldMatrix = matrix44.create_identity()
		self.dirty = True
	
	def SetPosition(self, x=None, y=None, z=None):
		if x is not None:
			self.position.x = x
		if y is not None:
			self.position.y = y
		if z is not None:
			self.position.z = z

	def SetRotation(self, angle):
		self.rotation = quaternion.create_from_z_rotation(self.rotAngle)

	def _CreateMatrix(self):
		self.worldMatrix = matrix44.multiply(
								matrix44.create_from_translation(self.position), 
								matrix44.create_from_quaternion(self.rotation)
							)

	def GetWorldMatrix(self):
		if self.dirty:
			self._CreateMatrix()
		return self.worldMatrix


