import bge
from bge import logic
import mathutils
import os

bge.render.setBackgroundColor([0,0,0,0])

scene = logic.getCurrentScene()	

# Set Initial Camera View to Top View
cam = scene.active_camera 
camPose = mathutils.Euler((0,0,0),'XYZ') 
cam.worldPosition = [0, 0, 15]
cam.worldOrientation = camPose


def show():
	cubeController = logic.getCurrentController()
	cubeOwn = cubeController.owner

	def Init():
		if not 'init' in cubeOwn:
			cubeOwn['init'] =1 

	#Load the meshes corresponding to the step_num		
	def Update():
		pass

	Init()
	Update()