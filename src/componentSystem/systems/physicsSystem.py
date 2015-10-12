import pypybox2d as b2
from pypybox2d.common import *

from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentConst import PHYSICS_COMPONENT

class PhysicsSystem(object):

	def __init__(self):
		self.world = b2.World((0, -30), True)

	def Setup(self):
		for physicsComponent in COMPONENT_REGISTRY.GetComponentsWithName(PHYSICS_COMPONENT):
			physicsType = physicsComponent.type
			position = physicsComponent.position
			shapes = physicsComponent.shapes
			physicsComponent.AddBody( self.CreateBody(physicsType, shapes, position) )

	def CreateBody(self, bodyType, shapes, position):
		body = None
		if bodyType == "static":
			body = self.world.create_static_body(position=position)
		elif bodyType == "dynamic":
			body = self.world.create_dynamic_body(position=position)
		elif bodyType == "kinematic":
			body = self.world.create_kinematic_body(position=position)

		for shapeInfo in shapes:
			shapeType = shapeInfo["type"]
			if shapeType == "box":
				halfwidth, halfheight = shapeInfo["width"] * 0.5, shapeInfo["height"] * 0.5
				body.create_polygon_fixture(box=(halfwidth, halfheight), friction=1, density=20)

		return body

	def Update(self, dt):
		self.world.step(dt, 10, 10)