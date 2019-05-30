# Sebastián Galindo 15452
# Gráficas por computadora
# Código obtenido de http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm

import copy
from glm import *
from Bitmap import *
from Lib import *
from object import *

screen = None
viewPort = {"x": 0, "y": 0, "width": 0, "heigth": 0}
blue = color(0, 0, 255)
red = color(255, 0, 0)
green = color(0, 255, 0)
colorStandard = 255
vertexBuffer = []
zBuffer = []
surface = Texture("PenguinTexture.bmp")

sign = lambda a: (a > 0) - (a < 0)

def glInit():
    pass


def glCreateWindow(width, heigth):
    global screen
    screen = Bitmap(width, heigth)


def glViewPort(x, y, width, heigth):
    global viewPort, zBuffer
    viewPort["x"] = x
    viewPort["y"] = y
    viewPort["width"] = width
    viewPort["heigth"] = heigth
    zBuffer = [[-999 for x in range(0, width+ 1)] for y in range(0, heigth + 1)]


def glClear():
    screen.clear()


def glClearColor(r, g, b):
    screen.clearColor = color(r, g, b)


# Recibe parametros entre -1 y 1
def glVertex(x, y):
    global viewPort
    global screen
    newX = int((x + 1) * (viewPort["width"] / 2) + viewPort["x"])
    newY = int((y + 1) * (viewPort["heigth"] / 2) + viewPort["y"])
    screen.point(newX, newY, screen.currentColor)


def glColor(r, g, b):
    r = int(r * colorStandard)
    g = int(g * colorStandard)
    b = int(b * colorStandard)
    screen.currentColor = color(r, g, b)


def glLine(x0, y0, x1, y1):
    global viewPort
    global screen
    x0, y0 = normalize(x0, y0, viewPort)
    x1, y1 = normalize(x1, y1, viewPort)

    # Setup initial conditions
    dx = x1 - x0
    dy = y1 - y0

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
        swapped = True

    # Recalculate differentials
    dx = x1 - x0
    dy = y1 - y0

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y0 < y1 else -1

    # Iterate over bounding box generating points between start and end
    y = y0
    points = []
    for x in range(x0, x1 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()

    for point in points:
        screen.point(point[0], point[1], screen.currentColor)


def glFinish():
    screen.write('high.bmp')



def transform(v1):
    vertex = vec3(*v1)
    vertex = vec4(vertex, 1)
    i = mat4(1)
    translateM = translate(i, vec3(0, -1300, -200))
    rotationM = rotate(i, 0.29, (1,0,0))
    scaleM = scale(i, (1400, 1400, 1400))
    modelM = translateM * rotationM * scaleM
    viewM = lookAt(vec3(0,0,200), vec3(0,0,0), vec3(0,1,0))

    projectM = mat4(
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, -0.001,
        0, 0, 0, 1
    )

    viewPortM = mat4(
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        viewPort["width"]/2, viewPort["heigth"]/2, 128, 1
    )
    vertex = viewPortM * projectM * viewM * modelM * vertex
    vertex = vec3(vertex/vertex.w)
    #print(vertex)
    return vertex


def glLoad(name, scale, translateX, translateY, translateZ):
    global screen, vertexBuffer
    model = Obj(name)
    for face in model.vfaces:
        vcount = len(face)
        for j in range(vcount):
            f1 = face[j][0] #vertex value
            t1 = face[j][1] #texture value
            n1 = face[j][2] #normal value
            v1 = copy.copy(model.vertices[f1 - 1])
            vt1 = copy.copy(model.vtextures[t1 - 1])
            vn1 = copy.copy(model.vnormals[n1 - 1])
            # v1 = [(x * scale) + translateX for x in v1]
            #v1[0] = (v1[0] * scale) + translateX
            #v1[1] = (v1[1] * scale) + translateY
            #v1[2] = (v1[2] * scale) + translateZ
            vertex = transform(v1)
            vertexBuffer.append(vertex)
            vertexBuffer.append(vt1)
            vertexBuffer.append(vn1)
    vertexBuffer = iter(vertexBuffer)

def length(v0):
  return (v0[0]**2 + v0[1]**2 + v0[2]**2)**0.5

def norm(v0):
    v0length = length(v0)

    if not v0length:
        return [0, 0, 0]

    return [v0[0] / v0length,
            v0[1] / v0length,
            v0[2] / v0length]

def cross(v1, v2):
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]

def dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def barycentric(A, B, C, P):
    v1 = [C[0] - A[0], B[0] - A[0], A[0] - P[0]]
    v2 = [C[1] - A[1], B[1] - A[1], A[1] - P[1]]

    b = cross(v1, v2)

    if(abs(b[2]) < 1):
        return -1, -1, -1

    return (1 - (b[0] + b[1]) / b[2], b[1] / b[2], b[0] / b[2])

def sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]

def getPixels(x, y):
    global viewPort
    newX = int((x + 1) * (viewPort["width"] / 2) + viewPort["x"])
    newY = int((y + 1) * (viewPort["heigth"] / 2) + viewPort["y"])
    return newX, newY

def shader(nA, nB, nC, w, v, u, light, surface_color):
    nx = float(nA[0]) * float(w) + float(nB[0]) * float(v) + float(nC[0]) * float(u)
    ny = float(nA[1]) * float(w) + float(nB[1]) * float(v) + float(nC[1]) * float(u)
    nz = float(nA[2]) * float(w) + float(nB[2]) * float(v) + float(nC[2]) * float(u)

    intensity = dot(light, (nx, ny, nz))
    return bytes(map(lambda b: int(b * intensity) if b * intensity > 0 else 0, surface_color))

def glTriangle():
    global vertexBuffer, viewPort, zBuffer, surface
    A = next(vertexBuffer)
    tA = next(vertexBuffer)
    nA = next(vertexBuffer)
    B = next(vertexBuffer)
    tB = next(vertexBuffer)
    nB = next(vertexBuffer)
    C = next(vertexBuffer)
    tC = next(vertexBuffer)
    nC = next(vertexBuffer)

    light = [0,0,1]
    normal = norm(cross(sub(B, A), sub(C, A))) #Falta el norm
    intensity = dot(light, normal)


    sortedX = sorted((A[0], B[0], C[0]))
    sortedY = sorted((A[1], B[1], C[1]))

    minX = int(sortedX[0])
    minY = int(sortedY[0])
    maxX = int(sortedX[-1])
    maxY = int(sortedY[-1])
    #print(minX, maxX)
    #assert False, (minX, mi)

    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            w, v, u = barycentric(A, B, C, [x, y])
            if u >= 0 and v >= 0 and w >= 0:
                z = w * A[2] + v * B[2] + u * C[2]
                tx = float(tA[0]) * float(w) + float(tB[0]) * float(v) + float(tC[0]) * float(u)
                ty = float(tA[1]) * float(w) + float(tB[1]) * float(v) + float(tC[1]) * float(u)
                surface_color = surface.get_color(tx, ty, 1)
                #surface_color = color(0,255,255)
                if 0 < x < viewPort["width"] and  0 < y < viewPort["heigth"] and zBuffer[y][x] < z:
                    shader_color = shader(nA, nB, nC, w, v, u, light, surface_color)
                    screen.point(x, y, shader_color)
                    zBuffer[y][x] = z
            #algoritmo para cambiar color del punto dependiendo de la direccion de la luz

def glDraw():
    while True:
        try:
            glTriangle()
        except StopIteration:
            break
