from OpenGL.GL import *
from renderables.renderObject import RenderObject

def CreateSquare(edgeLength, shaderResPath):
	dro = RenderObject(shaderResPath)
	dro.SetDrawInfo(GL_TRIANGLES, 6)

	halfEdge = edgeLength/2.0
	vertexData = [
		-halfEdge, -halfEdge,
		-halfEdge, halfEdge,
		halfEdge, halfEdge, 
		halfEdge, halfEdge, 
		halfEdge, -halfEdge,
		-halfEdge, -halfEdge
	]

	dro.AddPerObjectData("vinPosition", GL_FLOAT, 2, vertexData)
	dro.ConstructRenderObject()

	return dro

def CreateTexturedSquare(edgeLength, shaderResPath, texture):
	dro = RenderObject(shaderResPath)
	dro.SetDrawInfo(GL_TRIANGLES, 6)

	halfEdge = edgeLength/2.0
	vertexData = [
		-halfEdge, -halfEdge,
		-halfEdge, halfEdge,
		halfEdge, halfEdge, 
		halfEdge, halfEdge, 
		halfEdge, -halfEdge,
		-halfEdge, -halfEdge
	]

	uv = [
		0.0, 1.0,
		0.0, 0.0, 
		1.0, 0.0,
		1.0, 0.0, 
		1.0, 1.0,
		0.0, 1.0,
	]

	dro.AddPerObjectData("vinPosition", GL_FLOAT, 2, vertexData)
	dro.AddPerObjectData("vinUV", GL_FLOAT, 2, uv)
	dro.AddTexture(texture, 0)
	
	dro.ConstructRenderObject()

	return dro	
