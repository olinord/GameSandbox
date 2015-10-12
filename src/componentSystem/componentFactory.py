from componentSystem.componentConst import *

def CreateRenderableComponent(entityName, componentInfo):
	# import the components as late as possible, so we don't import gunk in the unit tests
	from componentSystem.components.renderable import RenderableComponent
	return RenderableComponent(entityName, componentInfo)

def CreatePlayerControlledComponent(entityName, componentInfo):
	# import the components as late as possible, so we don't import gunk in the unit tests
	from componentSystem.components.playerControlled import PlayerControlledComponent
	return PlayerControlledComponent(entityName, componentInfo)

def CreatePhysicsComponent(entityName, componentInfo):
	from componentSystem.components.physics import PhysicsComponent
	return PhysicsComponent(entityName, componentInfo)

def CreateBoxCollider(entityName, componentInfo):
	from componentSystem.components.subComponents.physics.boxCollider import BoxCollider
	return BoxCollider(entityName, componentInfo)

class ComponentNotFoundException(Exception):
	pass

class SubComponentNotFoundException(Exception):
	pass

componentFactoryMethods = {
	RENDERABLE_COMPONENT: CreateRenderableComponent,
	PLAYER_CONTROLLED_COMPONENT: CreatePlayerControlledComponent,
	PHYSICS_COMPONENT: CreatePhysicsComponent
}

def CreateComponent(entityName, componentName, componentInfo):
	try:
		return componentFactoryMethods[componentName](entityName, componentInfo)
	except KeyError:
		raise ComponentNotFoundException("Could not find component method for %s"%componentName)

subComponentFactoryMethods = {
}

def CrateSubComponent(entityName, subComponentName, subComponentInfo):
	try:
		return subComponentFactoryMethods[subComponentName](entityName, subComponentInfo)
	except KeyError:
		raise SubComponentNotFoundException("Could not find subcomponent method for %s"%subComponentName)