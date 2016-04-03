import sdl2
from sdl2 import video

from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_array_object import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def CreateWindow(width, height, windowName):
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return None, None

    window = sdl2.SDL_CreateWindow(windowName,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   width,
                                   height,
                                   sdl2.SDL_WINDOW_OPENGL|sdl2.SDL_WINDOW_RESIZABLE)
    if not window:
        print(sdl2.SDL_GetError())
        return None, None

    # Force OpenGL 3.3 'core' context.
    # Must set *before* creating GL context!
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
        video.SDL_GL_CONTEXT_PROFILE_CORE)
    video.SDL_GL_SetAttribute(video.SDL_GL_DOUBLEBUFFER, 1)
    video.SDL_GL_SetSwapInterval(1)

    context = sdl2.SDL_GL_CreateContext(window)

    return window, context

def ClearBuffers(backgroundColor):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*backgroundColor)

def SwapBuffers(window):
    sdl2.SDL_GL_SwapWindow(window)

def GetWindowEventHandler():
    return sdl2.SDL_Event()

def PollEvent(event):
    return sdl2.SDL_PollEvent(ctypes.byref(event))

def GetFrameTime():
    return sdl2.SDL_GetTicks()

def CloseWindow(window, context):
    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
