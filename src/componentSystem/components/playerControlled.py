from componentSystem.components.component import Component

class PlayerControlledComponent(Component):

	def __init__(self, entityName, componentInfo):
		Component.__init__(self, entityName, componentInfo)

	def Update(self, dt):
		pass