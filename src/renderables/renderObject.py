from OpenGL.GL import *
from OpenGL.arrays import *
from OpenGL.GL.ARB.vertex_array_object import *
from OpenGL.GL.shaders import *

from utilities.shaderManager import GetProgramWithGeneratedShaderNames, CreateImageTexture
from utilities.resourceManager import LoadImage
from pyrr import matrix44, vector3

class RenderObject(object):

	def __init__(self, shaderResPath):
		self.shaderResPath = shaderResPath
		self.shaderProgramID = None
		self.vaoId = None
		self.position = (0.0, 0.0)
		self.rotation = 0.0
		self.worldMatrix = None
		self.isDirty = True
		self.vertexInfo = []
		self.textures = []
		self.uniformDataLocations = {}
		self.primitiveType = None
		self.primitiveCount = -1

	def SetDrawInfo(self, primitiveType, primitiveCount):
		"""
		primitiveType: GL_TRIANGLES, GL_POINTS
		primitiveCount: The amount of primitives
		"""
		self.primitiveType = primitiveType
		self.primitiveCount = primitiveCount

	def AddPerObjectData(self, shaderInputName, inputType, inputSize, data):
		"""
		shaderInputName: the name that maps to a vertex shader input 
		inputType: GL_FLOAT/GL_INT or something 
		inputSize: 1 for a single input, 2 for a vector2, 3 for a vector3 etc
		data: a single array of what ever the inpuType is
		"""
		self.vertexInfo.append({
			"inputName": shaderInputName,
			"inputType": inputType,
			"inputSize": inputSize,
			"data": data
		})

	def AddTexture(self, textureResPath, textureIndex):
		self.textures.append( CreateImageTexture( LoadImage(textureResPath), GL_TEXTURE0 + textureIndex))

	def ConstructRenderObject(self):
		self.vaoId = glGenVertexArrays(1)
		glBindVertexArray(self.vaoId)

		self.shaderProgramID = GetProgramWithGeneratedShaderNames(self.shaderResPath)

		for i, vertexInfo in enumerate(self.vertexInfo):
			glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
			inputTypeSize = 4 if vertexInfo["inputType"] == GL_FLOAT else -1

			glBufferData(
				GL_ARRAY_BUFFER,
				inputTypeSize * len(vertexInfo["data"]),
				vbo.ArrayDatatype.asArray(vertexInfo["data"], vertexInfo["inputType"]),
				GL_STATIC_DRAW
			)

			glVertexAttribPointer(
				glGetAttribLocation(self.shaderProgramID, vertexInfo["inputName"]),
				vertexInfo["inputSize"],
				vertexInfo["inputType"],
				GL_FALSE,
				0,
				None
			)

			# Enable it on the shader program
			glEnableVertexAttribArray(i)

		# Clean up
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)

	def _GetUniformLocation(self, uniformAttributeName):
		uniformLocation = self.uniformDataLocations.get(uniformAttributeName, None)
		
		if uniformLocation is None:
			uniformLocation = glGetUniformLocation(self.shaderProgramID, uniformAttributeName)
			self.uniformDataLocations[uniformAttributeName] = uniformLocation
		
		return uniformLocation

	def SetPosition(self, x, y):
		self.position = (x, y)
		self.isDirty = True

	def SetRotation(self, rot):
		self.rotation = rot
		self.isDirty = True

	def SetUniformMatrix4fv(self, uniformAttributeName, matrixValue):
		uniformLocation = self._GetUniformLocation(uniformAttributeName)
		glUniformMatrix4fv(uniformLocation, 1, GL_FALSE, matrixValue)		

	def GetWorldMatrix(self):
		if self.worldMatrix is None or self.isDirty:
			self.isDirty = False
			translation = matrix44.create_from_translation(vector3.create(self.position[0], self.position[1], 0.0))
			rotation = matrix44.create_from_z_rotation(self.rotation)
			self.worldMatrix = matrix44.multiply(rotation, translation)

		return self.worldMatrix

	def Render(self, dt):
		self.SetUniformMatrix4fv("world", self.GetWorldMatrix())

		for textureID, textureIndex in self.textures:
			glActiveTexture(textureIndex);
			glBindTexture(GL_TEXTURE_2D, textureID);
		
		glBindVertexArray(self.vaoId)
		glDrawArrays(GL_TRIANGLES, 0, self.primitiveCount)

		glBindVertexArray(0)
		glUseProgram(0)
