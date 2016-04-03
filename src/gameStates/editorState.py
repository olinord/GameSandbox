from utilities.resourceManager import LoadEntityType
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentConst import PLAYER_CONTROLLED_COMPONENT, TRANSFORM_COMPONENT
from utilities.entityLoader import RegisterEntity
from componentSystem.systems.renderSystem import RenderSystem
from componentSystem.systems.physicsSystem import PhysicsSystem

class EditorState(object):

	def __init__(self):
		self.renderSystem = RenderSystem()

	def AddEntity(self, name, entityType):
		entity = LoadEntityType(entityType)
		entity[TRANSFORM_COMPONENT] = {"pos": (0.0, 0.0, 0.0), "rotAngle": 0.0}
		RegisterEntity(name, entity)

	def Resize(self, width, height):
		self.renderSystem.SetPerspective(width, height)

	def Update(self, dt):
		self.renderSystem.Update(dt)

	def Render(self, dt):
		self.renderSystem.Render(dt)