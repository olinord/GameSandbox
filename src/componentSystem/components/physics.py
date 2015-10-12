from componentSystem.components.component import Component
from pyrr import matrix44, vector3

class PhysicsComponent(Component):
	__requiredAttributes__ = ["type", "shapes"]
	__attributesWithDefaultValues__ = {"position": (0.0, 0.0), "rotation": (0.0)}

	def __init__(self, entityName, componentInfo):
		Component.__init__(self, entityName, componentInfo)
		self.body = None
		self.worldMatrix = None

	def CreateWorldMatrix(self):
		translation = matrix44.create_from_translation(vector3.create(self.body.position[0], self.body.position[1], 0.0))
		rotation = matrix44.create_from_z_rotation(-self.body.angle)

		return matrix44.multiply(rotation, translation)

	def AddBody(self, body):
		self.body = body
		self.worldMatrix = self.CreateWorldMatrix()

	def GetWorldMatrix(self):
		if self.body.awake:
			self.worldMatrix = self.CreateWorldMatrix()
		return self.worldMatrix

	def Update(self, dt):
		pass
		