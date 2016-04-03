from utilities.resourceManager import LoadResFile
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentConst import PLAYER_CONTROLLED_COMPONENT
from utilities.entityLoader import RegisterLevelEntities
from componentSystem.systems.renderSystem import RenderSystem
from componentSystem.systems.physicsSystem import PhysicsSystem

class LevelState(object):

	def __init__(self, levelName):
		self.levelData = LoadResFile("data/levels/" + levelName + ".yaml")
		self.renderSystem = RenderSystem()
		self.physicsSystem = PhysicsSystem()
		RegisterLevelEntities(self.levelData)
		self.physicsSystem.Setup()

	def Resize(self, width, height):
		self.renderSystem.SetPerspective(width, height)

	def Update(self, dt):
		playerControlledComponents = COMPONENT_REGISTRY.GetComponentsWithName(PLAYER_CONTROLLED_COMPONENT)
		for pcc in playerControlledComponents:
			pcc.Update(dt)
			
		self.physicsSystem.Update(dt)
		self.renderSystem.Update(dt)

	def Render(self, dt):
		self.renderSystem.Render(dt)
