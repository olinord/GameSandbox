
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from utilities.resourceManager import LoadEntityType, LoadResFile

def RegisterLevelEntities(levelData, entityLoader=None):
	if entityLoader is None:
		entityLoader = LoadEntityType

	for entityName, entityData in levelData["objects"].iteritems():
		entityInfo = entityLoader(entityData["type"])

		entityInfo.update(entityData.get("additionalComponents", {}))
		for componentName, newComponentData in entityData.get("overriddenComponents", {}).iteritems():
			if isinstance(newComponentData, dict):
				entityInfo[componentName].update(newComponentData)
			else:
				entityInfo[componentName] = newComponentData

		COMPONENT_REGISTRY.RegisterEntity(entityName, entityInfo)

def RegisterEntity(name, entityData):
	COMPONENT_REGISTRY.RegisterEntity(name, entityData)
