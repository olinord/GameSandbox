
from OpenGL.GL import *
from pyrr import Matrix44, Vector3, vector3, vector
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentConst import RENDERABLE_COMPONENT, TRANSLATION_COMPONENT

CAMERA_FOV = 45
CAMERA_NEAR = 10
CAMERA_FAR = 300

class RenderSystem(object):

	def __init__(self):
		self.renderBatches = {}
		self.view = Matrix44.identity()
		self.AdjustView((0.0, 0.0, -150), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
		self.perspectiveMatrix = Matrix44.identity()

	def AdjustView(self, eyePosition, targetPosition, upVector):
		eye = Vector3(eyePosition)
		target = Vector3(targetPosition)
		up = Vector3(upVector)
		zaxis = vector.normalise(eye - target)    # The "forward" vector.
		xaxis = vector.normalise(vector3.cross(up, zaxis))# The "right" vector.
		yaxis = vector3.cross(zaxis, xaxis)     # The "up" vector.

		# Create a 4x4 view matrix from the right, up, forward and eye position vectors
		self.view.r1 = [xaxis[0], yaxis[0], zaxis[0], 0]
		self.view.r2 = [xaxis[1], yaxis[1], zaxis[1], 0]
		self.view.r3 = [xaxis[2], yaxis[2], zaxis[2], 0]
		self.view.r4 =[-vector3.dot( xaxis, eye ), -vector3.dot( yaxis, eye ), -vector3.dot( zaxis, eye ),  1 ]
		 
		return self.view

	def SetPerspective(self, width, height):
		self.perspectiveMatrix = Matrix44.perspective_projection(CAMERA_FOV, width/height, CAMERA_NEAR, CAMERA_FAR)

		translationComponents = COMPONENT_REGISTRY.GetComponentsWithName(TRANSLATION_COMPONENT)
		for translationComponent in translationComponents:
			translationComponent.SetScale(1.0, (1.0 * width)/(1.0 * height))

	def Setup(self):
		for renderComponent in COMPONENT_REGISTRY.GetComponentsWithName(RENDERABLE_COMPONENT):
			batch = self.renderBatches.get(renderComponent.programID, [])
			batch.append(renderComponent)
			self.renderBatches[renderComponent.programID] = batch

	def Update(self, dt):
		pass

	def Render(self, dt):
		for programID, renderBatch in self.renderBatches.iteritems():
			glUseProgram(programID)
			renderBatch[0].SetPerFrameInfo(
				matrix44={"perspective":self.perspectiveMatrix, "view":self.view}
			)
			for renderComponent in renderBatch:
				renderComponent.Render(dt)
		glUseProgram(0)		
