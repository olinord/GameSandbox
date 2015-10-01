
import unittest
from mock import MagicMock
from utilities.levelLoader import RegisterLevelEntities
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentFactory import componentFactoryMethods

def CreateTestComponent1(componentInfo):
	return componentInfo

def CreateTestComponent2(componentInfo):
	return componentInfo

componentFactoryMethods["testComponent1"] = CreateTestComponent1
componentFactoryMethods["testComponent2"] = CreateTestComponent2


class RegisterLevelEntitiesTest(unittest.TestCase):


	def tearDown(self):
		COMPONENT_REGISTRY.RemoveAll()

	def test_thatLoadingLevelsWillRegisterAllEntitiesWithinTheLevel(self):
		levelData = {
			"name": "Bloo",
			"objects": {
				"boxy": {
					"type": "box",
				}
			}
		}
		boxData = {
			"testComponent1": "componentData"
		}

		RegisterLevelEntities(levelData, entityLoader=MagicMock(return_value=boxData))

		self.assertIn("boxy", COMPONENT_REGISTRY.GetAllEntities())
		self.assertEquals(boxData, COMPONENT_REGISTRY.GetEntityByName("boxy"))

	def test_thatLoadingLevelAllowsAddingNewComponentsToEntities(self):
		levelData = {
			"name": "Bloo",
			"objects": {
				"boxy": {
					"type": "box", 
					"additionalComponents": {
						"testComponent2": {"x": 10, "y": 20}
					}
				}
			}
		}
		baseBoxData = {
			"testComponent1": "renderableData"		
		}
		expectedBoxData = {
			"testComponent1": "renderableData",
			"testComponent2": {"x": 10, "y": 20}
		}

		RegisterLevelEntities(levelData, entityLoader=MagicMock(return_value=baseBoxData))

		registeredEntity = COMPONENT_REGISTRY.GetEntityByName("boxy")

		self.assertEquals(expectedBoxData, registeredEntity)

	def test_thatLoadingLevelAllowsOverridingComponentsOfEntities(self):
		levelData = {
			"name": "Bloo",
			"objects": {
				"boxy": {
					"type": "box", 
					"overriddenComponents": {
						"testComponent1": "newAgeRenderableStuff"
					}
				}
			}
		}
		baseBoxData = {
			"testComponent1": "renderableData"		
		}
		expectedBoxData = {
			"testComponent1": "newAgeRenderableStuff"
		}

		RegisterLevelEntities(levelData, entityLoader=MagicMock(return_value=baseBoxData))

		registeredEntity = COMPONENT_REGISTRY.GetEntityByName("boxy")

		self.assertEquals(expectedBoxData, registeredEntity)


if __name__ == '__main__':
    unittest.main()
