from componentSystem.components.component import Component

class CharacterComponent(Component):
	__requiredAttributes__ = ["maxSpeed"]

	def __init__(self, entityName, componentInfo):
		Component.__init__(self, entityName, componentInfo)
		
