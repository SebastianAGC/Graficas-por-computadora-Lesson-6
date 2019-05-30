from sr6 import *


glInit()
glCreateWindow(1000, 1000)
glViewPort(0, 0, 1000, 1000)
glClearColor(200, 200, 255)
glClear()
glLoad("PenguinBaseMesh.obj", 800, 500, 25, 0)
glDraw()
glFinish()

