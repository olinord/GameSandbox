from OpenGL.GL import *
from OpenGL.arrays import *
from OpenGL.GL.ARB.vertex_array_object import *
from OpenGL.GL.shaders import *

from utilities.resourceManager import LoadImage
from utilities.shaderManager import GetProgram, CreateImageTexture
from componentSystem.componentRegistry import COMPONENT_REGISTRY
from componentSystem.componentConst import PHYSICS_COMPONENT
from componentSystem.components.component import Component


class ModelComponent(Component):
	__requiredAttributes__ = ["name", "texture", "width", "height", "offset"]
	
	def __init__(self, entityName, componentInfo):
		Component.__init__(self, entityName, componentInfo)
		image = LoadImage(self.imageResFile)
		self.halfHeight = self.height * 0.5
		self.halfWidth = self.width * 0.5
		
		self.imageID, _ = CreateImageTexture(image)
		self.vaoId = None
		self.programID = None

		self.physicsComponent = None
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
			-self.halfWidth, -self.halfHeight,
			-self.halfWidth, self.halfHeight,
			self.halfWidth, self.halfHeight, 
			self.halfWidth, self.halfHeight, 
			self.halfWidth, -self.halfHeight,
			-self.halfWidth, -self.halfHeight
		]

		uv = [
			0.0, 1.0,
			0.0, 0.0, 
			1.0, 0.0,
			1.0, 0.0, 
			1.0, 1.0,
			0.0, 1.0,
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
			4 * len(uv),
			vbo.ArrayDatatype.asArray(uv, GL_FLOAT),
			GL_STATIC_DRAW
		)

		glVertexAttribPointer(
			glGetAttribLocation(self.programID, 'vinUV'),
			2,
			GL_FLOAT,
			GL_FALSE,
			0,
			None
		)

		# Enable it on the shader program
		glEnableVertexAttribArray(1)

		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)

	def SetPerFrameInfo(self, matrix44={}):
		for matrixName, matrixValue in matrix44.iteritems():
			glUniformMatrix4fv(self.uniformDataLocations[matrixName], 1, GL_FALSE, matrixValue)
	
	def GetWorldMatrix(self):
		if self.physicsComponent is None:
			self.physicsComponent = COMPONENT_REGISTRY.GetEntityComponent(self.entityName, PHYSICS_COMPONENT)
		return self.physicsComponent.GetWorldMatrix()

	def Render(self, dt):
		self.SetPerFrameInfo(matrix44={"world": self.GetWorldMatrix()})

		glActiveTexture(GL_TEXTURE0);
		glBindTexture(GL_TEXTURE_2D, self.imageID);
		
		glBindVertexArray(self.vaoId)
		glDrawArrays(GL_TRIANGLES, 0, 6)

		glBindVertexArray(0)
