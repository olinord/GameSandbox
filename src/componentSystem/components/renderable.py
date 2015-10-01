

from OpenGL.GL import *
from OpenGL.arrays import *
from OpenGL.GL.ARB.vertex_array_object import *
from OpenGL.GL.shaders import *

from utilities.shaderManager import GetProgram
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentConst import TRANSLATION_COMPONENT


class RenderableComponent(object):

	def __init__(self, entityName, componentInfo):
		self.width = componentInfo["width"]
		self.height = componentInfo["height"]
		self.entityName = entityName
		self.vaoId = None
		self.programID = None

		self.translationComponent = None
		self.uniformDataLocations = {}

		self.SetupRenderInfo()

	def SetupRenderInfo(self):
		self.SetVertexArrayObject()
		self.SetupShaders()
		self.SetupRenderingData()

	def SetVertexArrayObject(self):
		# creates the rendering data so it can be shipped over to the GPU
		self.vaoId = glGenVertexArrays(1)
		glBindVertexArray(self.vaoId)

	def SetupShaders(self):

		self.programID = GetProgram("generic.vs", "generic.ps")

		self.uniformDataLocations = {
			attributeName: glGetUniformLocation(self.programID, attributeName)
			for attributeName in ["world", "view", "perspective"]
		}

	def SetupRenderingData(self):
		vertexBufferIDs = glGenBuffers(2)

		points = [
			0.0, 0.0,
			0.0, 1.0,
			1.0, 1.0, 
		]

		# Create the vertex array for the data
		glBindBuffer(GL_ARRAY_BUFFER, vertexBufferIDs[0])
		glBufferData(
			GL_ARRAY_BUFFER,
			 4 * len(points),
			 vbo.ArrayDatatype.asArray(points, GL_FLOAT),
			 GL_STATIC_DRAW
		)

		glVertexAttribPointer(
			glGetAttribLocation(self.programID, 'vinPosition'),
			2,
			GL_FLOAT,
			GL_FALSE,
			0,
			None
		)

		# Enable it on the shader program
		glEnableVertexAttribArray(0)

		glBindBuffer(GL_ARRAY_BUFFER, vertexBufferIDs[1])
		glBufferData(
			GL_ARRAY_BUFFER,
			4 * len(points),
			vbo.ArrayDatatype.asArray([(1.0, 1.0, 1.0, 1.0)]*len(points), GL_FLOAT),
			GL_STATIC_DRAW
		)

		glVertexAttribPointer(
			glGetAttribLocation(self.programID, 'vinColor'),
			4,
			GL_FLOAT,
			GL_FALSE,
			0,
			None
		)

		# Enable it on the shader program
		glEnableVertexAttribArray(1)

		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)

	def SetPerFrameInfo(self, **kwargs):
		for argumentName, argumentValue in kwargs.iteritems():
			glUniformMatrix4fv(self.uniformDataLocations[argumentName], 1, GL_FALSE, argumentValue)

	def GetWorldMatrix(self):
		if self.translationComponent is None:
			self.translationComponent = COMPONENT_REGISTRY.GetEntityComponent(self.entityName, TRANSLATION_COMPONENT)
		return self.translationComponent.matrix

	def Render(self, dt):
		glUniformMatrix4fv(self.uniformDataLocations["world"], 1, GL_FALSE, self.GetWorldMatrix())
		glBindVertexArray(self.vaoId)
		glDrawArrays(GL_TRIANGLES, 0, 3)

		glBindVertexArray(0)
