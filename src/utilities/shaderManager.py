
from OpenGL.GL.shaders import *
from OpenGL.GL import *
from utilities.resourceManager import ABSOLUTE_RES_FOLDER, AbsJoin

SHADER_FOLDER = AbsJoin(ABSOLUTE_RES_FOLDER, "shaders")

cachedShaderPrograms = {}

def GetProgram(vertexShaderPath, pixelShaderPath):
	cacheKey = (vertexShaderPath, pixelShaderPath)

	if cacheKey not in cachedShaderPrograms:
		# setup the shaders used for the rendering
		vertexShader = LoadShader(vertexShaderPath)
		pixelShader = LoadShader(pixelShaderPath)

		programID = compileProgram(vertexShader, pixelShader)

		cachedShaderPrograms[cacheKey] = programID

		return programID
	return cachedShaderPrograms[cacheKey]

def LoadShader(shaderPath):
	shaderType = GL_VERTEX_SHADER
	if shaderPath.endswith(".gs"):
		shaderType = GL_GEOMETRY_SHADER
	elif shaderPath.endswith(".ps"):
		shaderType = GL_FRAGMENT_SHADER
		
	with open(AbsJoin(SHADER_FOLDER, shaderPath)) as f:
		return compileShader(f.read(), shaderType)

def CreateImageTexture(image):
	xSize, ySize, _ = image.shape
	
	textureID = glGenTextures(1)

	glActiveTexture(GL_TEXTURE0)
	glBindTexture(GL_TEXTURE_2D, textureID)

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

	glTexImage2D(
			GL_TEXTURE_2D, 0, GL_RGBA, xSize, ySize, 0,
			GL_RGBA, GL_UNSIGNED_BYTE, image.tobytes()
		)
	return textureID
