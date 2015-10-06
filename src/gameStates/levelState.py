from utilities.resourceManager import LoadResFile
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentConst import PLAYER_CONTROLLED_COMPONENT
from utilities.levelLoader import RegisterLevelEntities
from componentSystem.systems.renderSystem import RenderSystem

class LevelState(object):

	def __init__(self, levelName):
		self.levelData = LoadResFile("data/levels/" + levelName + ".yaml")
		RegisterLevelEntities(self.levelData)
		self.renderSystem = RenderSystem()
		self.renderSystem.Setup()

	def Resize(self, width, height):
		self.renderSystem.SetPerspective(width, height)

	def Update(self, dt):
		playerControlledComponents = COMPONENT_REGISTRY.GetComponentsWithName(PLAYER_CONTROLLED_COMPONENT)
		for pcc in playerControlledComponents:
			pcc.Update(dt)
		self.renderSystem.Update(dt)

	def Render(self, dt):
		self.renderSystem.Render(dt)
