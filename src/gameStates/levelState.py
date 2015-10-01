from utilities.resourceManager import LoadResFile
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentConst import RENDERABLE_COMPONENT, TRANSLATION_COMPONENT
from utilities.levelLoader import RegisterLevelEntities
from componentSystem.systems.renderSystem import RenderSystem

class LevelState(object):

	def __init__(self, levelName, renderSystem):
		self.levelData = LoadResFile("data/levels/" + levelName + ".yaml")
		RegisterLevelEntities(self.levelData)
		self.renderSystem = renderSystem
		self.renderSystem.Setup()


	def Update(self, dt):
		self.renderSystem.Update(dt)

	def Render(self, dt):
		self.renderSystem.Render(dt)
