
import sdl2
from sdl2 import video

from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_array_object import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from utilities.windowUtil import *
from gameStates.editorState import EditorState
from componentSystem.systems.renderSystem import RenderSystem

class EditorApp(object):

	MAX_FRAME_TIME = 1000.0/60.0

	def __init__(self):
		self.backgroundColor = (0.2, 0.2, 0.2, 1.0)
		self.window = None
		self.context = None
		self.currentState = None

	def SetupApp(self, width, height):
		self.window, self.context = CreateWindow(width, height, "Editor")
		if not self.window:
			return False
		
		self.currentState = EditorState()
		# Maybe have one state for each component?
		# translation, animatedRenderable, staticRenderable and finally one for the entity as a whole in a test level?
		self.currentState.AddEntity("test", "skeletonTest")
		self.Resize(width, height)

		return True

	def Run(self):
		running = True

		event = GetWindowEventHandler()

		lastFrameTime = GetFrameTime()
		currentFrameTime = lastFrameTime

		while running:
			currentFrameTime = GetFrameTime()
			dt = (currentFrameTime - lastFrameTime)

			# Cap FPS
			if dt < self.MAX_FRAME_TIME:
				sdl2.SDL_Delay(int(self.MAX_FRAME_TIME - dt))
				dt = self.MAX_FRAME_TIME
			dt *= 0.001
			lastFrameTime = currentFrameTime

			while PollEvent(event) != 0:
				if self.IsExitEvent(event):
					running = False
				elif self.IsWindowResizeEvent(event):
					self.Resize(event.window.data1, event.window.data2)
					
			ClearBuffers(self.backgroundColor)
			self.currentState.Update(dt)
			self.currentState.Render(dt)

			SwapBuffers(self.window)

		self.Exit()

	def IsExitEvent(self, event):
		"""
		Temporary check if the user wants to exit
		"""
		if event.type == sdl2.SDL_QUIT:
			return True
		elif event.type == sdl2.SDL_KEYDOWN:
			if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
				return True

		return False

	def IsWindowResizeEvent(self, event):
		return event.type == sdl2.SDL_WINDOWEVENT and event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED

	def IsToggleDebugModeEvent(self, event):
		if event.type == sdl2.SDL_KEYDOWN:
			if event.key.keysym.mod & sdl2.KMOD_LCTRL or event.key.keysym.mod & sdl2.KMOD_RCTRL:
				return event.key.keysym.sym == sdl2.SDLK_d

	def Resize(self, width, height):
		glViewport(0, 0, width, height)
		self.currentState.Resize(width, height)

	def Exit(self):
		CloseWindow(self.window, self.context)
