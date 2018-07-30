# Computer Graphics
# Assignment3
# 2014004893
# Dae In Lee

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamTrans = 0.
gCamHeight = 1.
gCamZoom = 1.
gMaxPos = 1.
normalSet = 0
isWireframe = True
objFile = None
vertexList = np.array([])
normalList = np.array([])
vertexElements = np.array([])
normalElements = np.array([])
indexIndicator = {}
indices = np.array([])

def render():
	global gCamAng, gCamHeight, gCamTrans, gCamZoom, gMaxPos
	global isWireframe, indices

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glEnable(GL_DEPTH_TEST)
	if isWireframe:
		glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
	else:
		glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 1, 1,gMaxPos*10)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(5*np.sin(gCamAng)*gCamZoom,(gCamHeight+gCamTrans)*gCamZoom,5*np.cos(gCamAng)*gCamZoom,
			  0,0,0, 0,1,0)

	# draw global frame
	drawFrame()

	# Enable Lighting
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHT1)
	glEnable(GL_LIGHT2)

	# set light properties
	lightPos0 = (gMaxPos*2,	0, 			0, 			1.)
	lightPos1 = (gMaxPos*2,	gMaxPos*2,	gMaxPos*2, 	1.)
	lightPos2 = (0, 		0,			gMaxPos*2,	1.)
	glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
	glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
	glLightfv(GL_LIGHT2, GL_POSITION, lightPos2)

	ambientLightColor0 = (0.5,0.,0.,1.)
	diffuseLightColor0 = (.6,0.,0.,1.)
	specularLightColor0 = (.7,.7,.7,1.)
	glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor0)
	glLightfv(GL_LIGHT0, GL_SPECULAR, specularLightColor0)
	ambientLightColor1 = (0.,.5,0.,1.)
	diffuseLightColor1 = (0.,0.6,0.,1.)
	specularLightColor1 = (.7,.7,.7,1.)
	glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
	glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor1)
	glLightfv(GL_LIGHT1, GL_SPECULAR, specularLightColor1)
	ambientLightColor2 = (0.,0.,.5,1.)
	diffuseLightColor2 = (0.,0.,.6,1.)
	specularLightColor2 = (.7,.7,.7,1.)
	glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor2)
	glLightfv(GL_LIGHT2, GL_DIFFUSE, diffuseLightColor2)
	glLightfv(GL_LIGHT2, GL_SPECULAR, specularLightColor2)

	# diffuseObjectColor = (1.,1.,1.,1.)
	# specularObjectColor = (1.,1.,1.,1.)
	# glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, diffuseObjectColor)

	# glScalef(0.5, 0.5, 0.5)
	glDrawElements(GL_TRIANGLES, indices.size, GL_UNSIGNED_INT, indices)

	glDisable(GL_LIGHTING)


def drawFrame():
	glBegin(GL_LINES)
	glColor3ub(255,0,0)
	glVertex3fv(np.array([0.,0.,0.]))
	glVertex3fv(np.array([1.,0.,0.]))
	glColor3ub(0,255,0)
	glVertex3fv(np.array([0.,0.,0.]))
	glVertex3fv(np.array([0.,1.,0.]))
	glColor3ub(0,0,255)
	glVertex3fv(np.array([0.,0.,0]))
	glVertex3fv(np.array([0.,0.,1.]))
	glEnd()

def key_callback(window, key, scancode, action, mods):
	global gCamAng, gCamHeight, gCamTrans, gCamZoom, isWireframe
	if action == glfw.PRESS or action==glfw.REPEAT:
		if key == glfw.KEY_1:
			gCamAng += np.radians(-10)
		elif key == glfw.KEY_2:
			gCamTrans += 0.1
		elif key == glfw.KEY_3:
			gCamAng += np.radians(10)
		elif key == glfw.KEY_W:
			gCamTrans -= 0.1
		elif key == glfw.KEY_A:
			if gCamZoom > 0.1:
				gCamZoom -= 0.1
		elif key == glfw.KEY_S:
			gCamZoom += 0.1
		elif key == glfw.KEY_Z:
			isWireframe = not isWireframe

def drop_callback(window, paths):
	global gMaxPos, objFile, vertexList, normalList, normalSet
	global vertexElements, normalElements, indices, indexIndicator

	if len(paths) > 1:
		print("cannot model more than 1 file at a time")
		return;

	fileName= getFileName(paths[0])
	if (fileName.split('.')[-1] != "obj"):
		print("not an OBJ file")
		return

	if objFile is not None:
		if objFile.name == paths[0]:	# If file is already displaying, just stay as it is.
			return
		objFile.close()

	objFile = open(paths[0], "r")
	vertexList = []
	normalList = []
	vertexElements = []
	normalElements = []
	indices = []
	gMaxPos = 1.0
	normalSet = 0
	indexIndicator.clear()
	totalFaces = triFaces = quadFaces = polyFaces = 0

	for line in objFile:
		split = line.split()

		if not len(split):
			continue
		if split[0] == "v":		# vertex
			vertexList.append([float(i) for i in split[1:]])
			gMaxPos = max(float(split[1]), float(split[2]), float(split[3]), gMaxPos)
		elif split[0] == "vn":	# texture
			normalList.append([float(i) for i in split[1:]])
		elif split[0] == "f":	# face
			cnt = len(split) - 1
			tmpIndex = []
			tmpNormal = []
			totalFaces += 1
			if cnt == 3:
				triFaces += 1
			elif cnt == 4:
				quadFaces += 1
			elif cnt >= 5:
				polyFaces += 1
			for i in range(1, cnt+1):
				cur = split[i].split('/')
				tmpIndex.append(int(cur[0])-1)
				if len(cur) >= 3:
					tmpNormal.append(int(cur[2])-1)
				else:
					tmpNormal.append(-1)

			firstIndex = elementsIndex(tmpIndex[0], tmpNormal[0])
			secondIndex = elementsIndex(tmpIndex[1], tmpNormal[1])
			for i in range(2, cnt):
				thirdIndex = elementsIndex(tmpIndex[i], tmpNormal[i])
				indices.append([firstIndex, secondIndex, thirdIndex])
				secondIndex = thirdIndex

	vertexElements = np.array(vertexElements)
	normalElements = np.array(normalElements)
	indices = np.array(indices)
	# print("vertex")
	# print(vertexElements)
	# print("normal")
	# print(normalElements)
	# print("index")
	# print(indices)
	if normalSet > 0:
		glEnableClientState(GL_NORMAL_ARRAY)
	else:
		glDisableClientState(GL_NORMAL_ARRAY)

	glVertexPointer(3, GL_DOUBLE, 3*vertexElements.itemsize, vertexElements)
	glNormalPointer(GL_DOUBLE, 3*normalElements.itemsize, normalElements)
	# print file information
	print(fileName)
	print("Total number of faces: %d" % totalFaces)
	print("Number of faces with 3 vertices: %d" % triFaces)
	print("Number of faces with 4 vertices: %d" % quadFaces)
	print("Number of faces with more than 4 vertices: %d" % polyFaces)
	print("")
	objFile.close()

def getFileName(path):
	return path.strip('/').strip('\\').split('/')[-1].split('\\')[-1]

def elementsIndex(vertex, normal):
	global vertexList, normalList, normalSet
	global vertexElements, normalElements, indexIndicator
	tmp = (vertex, normal)
	tmpVertex = vertexList[vertex]
	if normal == -1: # In case of normal vector is not specified.
		tmpNormal = [0., 0., 0.]
		normalSet -= 1
	else:
		tmpNormal = normalList[normal]
		normalSet += 1
	idx = indexIndicator.get(tmp)
	if idx is not None:
		return idx
	else:
		idx = indexIndicator.get('last', 0)
		indexIndicator['last'] = idx + 1
		indexIndicator[tmp] = idx
		vertexElements.append(tmpVertex)
		normalElements.append(tmpNormal)
		return idx

def main():
	if not glfw.init():
		return

	window = glfw.create_window(640,640,'2014004893',None,None)
	if not window:
		glfw.terminate()
		return

	glfw.make_context_current(window)
	glfw.set_key_callback(window,key_callback)
	glfw.set_drop_callback(window, drop_callback)
	glfw.swap_interval(1)

	glEnableClientState(GL_VERTEX_ARRAY)
	glEnableClientState(GL_NORMAL_ARRAY)
	while not glfw.window_should_close(window):
		glfw.poll_events()
		render()
		glfw.swap_buffers(window)

	glfw.terminate()

if __name__ =="__main__":
	main()
