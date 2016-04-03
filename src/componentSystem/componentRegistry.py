
"""
Entities are defined in yaml files and are of the following format

EntityName:
	ComponentName1: componentInfo
	ComponentName2: componentInfo
	...
"""

from collections import defaultdict
from componentSystem.componentFactory import CreateComponent

class ComponentRegistry(object):

	def __init__(self):
		# A dict of all compnents with a specific name {ComopnentName: [components]}
		self.componentsByName = defaultdict(list)
		self.entities = {}

	def GetAllEntities(self):
		return self.entities

	def GetComponentsWithName(self, componentName):
		return self.componentsByName[componentName]

	def GetEntityByName(self, entityName):
		return self.entities[entityName]

	def HasEntityComponent(self, entityName, componentName):
		return componentName in self.entities[entityName]

	def GetEntityComponent(self, entityName, componentName, default=None):
		try:
			return self.entities[entityName][componentName]
		except KeyError:
			return default

	def RegisterEntity(self, entityName, components):
		for componentName, componentInfo in components.iteritems():
			self.RegisterComponentForEntity(entityName, componentName, componentInfo)

	def RegisterComponentForEntity(self, entityName, componentName, componentInfo):
		entityComponents = self.entities.get(entityName, {})
		component = CreateComponent(entityName, componentName, componentInfo)
		entityComponents[componentName] = component
		self.entities[entityName] = entityComponents

		self.componentsByName[componentName].append(component)

	def RemoveEntity(self, entityName):
		for componentName, component in self.entities.get(entityName, {}).iteritems():
			self.componentsByName[componentName].remove(component)

		del self.entities[entityName]

	def RemoveAll(self):
		self.entities.clear()
		self.componentsByName.clear()


COMPONENT_REGISTRY = ComponentRegistry()
