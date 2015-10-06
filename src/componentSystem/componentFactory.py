from componentSystem.componentConst import *

def CreateRenderableComponent(entityName, componentInfo):
	# import the components as late as possible, so we don't import gunk in the unit tests
	from componentSystem.components.renderable import RenderableComponent
	return RenderableComponent(entityName, componentInfo)

def CreateTranslationComponent(entityName, componentInfo):
	# import the components as late as possible, so we don't import gunk in the unit tests
	from componentSystem.components.translation import TranslationComponent
	return TranslationComponent(entityName, componentInfo)

def CreatePlayerControlledComponent(entityName, componentInfo):
	# import the components as late as possible, so we don't import gunk in the unit tests
	from componentSystem.components.playerControlled import PlayerControlledComponent
	return PlayerControlledComponent(entityName, componentInfo)

componentFactoryMethods = {
	RENDERABLE_COMPONENT: CreateRenderableComponent,
	TRANSLATION_COMPONENT: CreateTranslationComponent,
	PLAYER_CONTROLLED_COMPONENT: CreatePlayerControlledComponent
}

def CreateComponent(entityName, componentName, componentInfo):
	try:
		return componentFactoryMethods[componentName](entityName, componentInfo)
	except KeyError:
		print "Could not find component method for %s"%componentName