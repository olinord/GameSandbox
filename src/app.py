
import sdl2
from sdl2 import video

from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_array_object import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from gameStates.levelState import LevelState
from componentSystem.systems.renderSystem import RenderSystem

class GameApp(object):

	def __init__(self, gameName):
		self.backgroundColor = (0.2, 0.2, 0.2, 1.0)
		self.gameName = gameName
		self.window = None
		self.context = None
		self.currentState = None

	def SetupApp(self, width, height):
		if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
			print(sdl2.SDL_GetError())
			return -1

		self.window = sdl2.SDL_CreateWindow(self.gameName,
									   sdl2.SDL_WINDOWPOS_UNDEFINED,
									   sdl2.SDL_WINDOWPOS_UNDEFINED,  
									   width, 
									   height,
									   sdl2.SDL_WINDOW_OPENGL|sdl2.SDL_WINDOW_RESIZABLE)
		if not self.window:
			print(sdl2.SDL_GetError())
			return -1

		# Force OpenGL 3.3 'core' context.
		# Must set *before* creating GL context!
		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
			video.SDL_GL_CONTEXT_PROFILE_CORE)
		video.SDL_GL_SetAttribute(video.SDL_GL_DOUBLEBUFFER, 1)
		video.SDL_GL_SetSwapInterval(1)

		self.context = sdl2.SDL_GL_CreateContext(self.window)

		self.currentState = LevelState("level1")
		self.Resize(width, height)

	def Run(self):
		event = sdl2.SDL_Event()
		running = True


		lastFrameTime = sdl2.SDL_GetTicks()
		currentFrameTime = lastFrameTime

		while running:
			currentFrameTime = sdl2.SDL_GetTicks()
			dt = (currentFrameTime - lastFrameTime)*0.0001
			
			while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
				if self.IsExitEvent(event):
					running = False
				elif self.IsWindowResizeEvent(event):
					self.Resize(event.window.data1, event.window.data2)

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			glClearColor(*self.backgroundColor)

			self.currentState.Update(dt)
			self.currentState.Render(dt)

			sdl2.SDL_GL_SwapWindow(self.window)
			lastFrameTime = currentFrameTime
			
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

	def Resize(self, width, height):
		self.currentState.Resize(width, height)

	def Exit(self):
		sdl2.SDL_GL_DeleteContext(self.context)
		sdl2.SDL_DestroyWindow(self.window)
		sdl2.SDL_Quit()
