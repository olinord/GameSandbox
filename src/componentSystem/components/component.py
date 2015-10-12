from componentSystem.componentFactory import CrateSubComponent


class InvalidAttributeException(Exception):
	def __init__(self, entityName, invalidAttributeName, invalidAttributeValue):
		self.invalidAttributeName = invalidAttributeName
		self.invalidAttributeValue = invalidAttributeValue
		self.entityName = entityName

	def __str__(self):
		return "['%s'] Invalid Attribute: '%s' with value '%s'" % (
			self.entityName, self.invalidAttributeName, self.invalidAttributeValue
			)

class RequiredAttributeMissingException(Exception):
	def __init__(self, entityName, requiredAttributeName):
		self.requiredAttributeName = requiredAttributeName
		self.entityName = entityName

	def __str__(self):
		return "['%s'] Missing Required Attribute: '%s'" % (self.entityName, self.invalidAttributeName)


class Component(object):
	__subComponents__ = {}
	__requiredAttributes__ = []
	__attributesWithDefaultValues__ = {}

	def __init__(self, entityName, componentInfo):
		self.entityName = entityName

		if componentInfo is not None:
			for attributeName, attributeValue in componentInfo.iteritems():
				if attributeName in self.__subComponents__:
					componentName = self.__subComponents__[attributeName]
					component = CrateSubComponent(entityName, componentName, attributeValue)
					setattr(self, attributeName, component)
				elif attributeName in self.__requiredAttributes__:
					setattr(self, attributeName, attributeValue)
				elif attributeName in self.__attributesWithDefaultValues__:
					setattr(self, attributeName, attributeValue)
				else:
					raise InvalidAttributeException(entityName, attributeName, attributeValue)

		for attributeName in self.__requiredAttributes__:
			if not hasattr(self, attributeName):
				raise RequiredAttributeMissingException(entityName, attributeName)				

		for attributeName, defaultAttributeValue in self.__attributesWithDefaultValues__.iteritems():
			if not hasattr(self, attributeName):
				setattr(self, attributeName, defaultAttributeValue)

				