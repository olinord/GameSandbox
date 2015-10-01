
from OpenGL.GL.shaders import *
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
