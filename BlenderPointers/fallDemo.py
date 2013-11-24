import jpc
import time
from bge import logic
import mathutils

class Pointers:
	arrow = 'arrowFlat'
	circle = 'circleArrow'
	cross = 'crossHair'

step_num = -1

#Parse the pre-compiled text file to receive data
stepFile = open('/home/bhala/DevTools/mrsd-gemini-blender/BlenderPointers/gemini_steps1.txt')
stepFileLine = list(stepFile)

stepNo =[0 for x in range(len(stepFileLine))]
stlFileIndex =[0 for x in range(len(stepFileLine))]
animateIndex =[0 for x in range(len(stepFileLine))]

objectPos = [ [0 for x in range(3)] for y in range(len(stepFileLine))]
objectPos = [ [0 for x in range(3)] for y in range(len(stepFileLine))]
objectAngles = [ [0 for x in range(3)] for y in range(len(stepFileLine))]
camPos = [ [0 for x in range(3)] for y in range(len(stepFileLine))]
camAngles = [ [0 for x in range(3)] for y in range(len(stepFileLine))]

for lineNo,line in enumerate(stepFileLine):
	thisLine = line.split()
	stepNo[lineNo] = int(thisLine[0])
	stlFileIndex[lineNo] = int(thisLine[1])
	animateIndex[lineNo] = int(thisLine[2])
	objectPos[lineNo] = [float(thisLine[3]),float(thisLine[4]),float(thisLine[5])]
	objectAngles[lineNo] = [float(thisLine[6]),float(thisLine[7]),float(thisLine[8])]
	camPos[lineNo] = [float(thisLine[9]),float(thisLine[10]),float(thisLine[11])]
	camAngles[lineNo] = [float(thisLine[12]),float(thisLine[13]),float(thisLine[14])]

#Get all the pointers - Load it from the blender File
logic.LibLoad("/home/bhala/DevTools/mrsd-gemini-blender/BlenderPointers/animateObjects.blend","Scene")

#Get the initial Scene
scene = logic.getCurrentScene()	

objList = scene.objects
objList[0].visible = False
objList[1].visible = True
objList[2].visible = True
			
objListStr = [str(x) for x in objList]

# Set Initial Camera View to Top View
cam = scene.active_camera 
camPose = mathutils.Euler((0,0,0),'XYZ') 
cam.worldPosition = [0, 0, 20]
cam.worldOrientation = camPose

#Connect to JSON Server
# print ('Connecting to Server..')
c = jpc.connect(host = 'localhost',port=50000)
s = jpc.Proxy(c)
# print ('Connected')

def renderStep():
	cubeController = logic.getCurrentController()
	cubeOwn = cubeController.owner

	def Init():
		if not 'init' in cubeOwn:
			cubeOwn['init'] =1 

	#Load the meshes corresponding to the step_num		
	def renderObject(step_num):
		global objList
		scene = logic.getCurrentScene()
		cube = scene.objects[0]

		pointerIdx = animateIndex[step_num[0]]

		if pointerIdx == 0:
			pointer = Pointers.arrow
		elif pointerIdx == 1:
			pointer = Pointers.circle
		else:
			pointer = Pointers.cross

		print ("Pointer is " + pointer)

		if pointer in objList:
			objIdx = objListStr.index(pointer)
			print ("Object Index " + str(objIdx))
		else:
			print("Pointer not Found")
		

		if objIdx == 3:
		 	objList[3].visible = True
		 	objList[4].visible = False
		 	objList[5].visible = False
		elif objIdx == 4:
			objList[3].visible = False
			objList[4].visible = True
			objList[5].visible = False
		else:
			objList[3].visible = False
			objList[4].visible = False
			objList[5].visible = True

		# for i in range(0,len(objList)):
		# 	if i == objIdx:
		# 		objList[objIdx].visible = True
		# 		print("In Initial")
		# 	else:
		# 		objList[objIdx].visible = False
		# 		print("offscreen")
		
	#Get the state from JSON Server
	def getState():

		global step_num, s

		curr_state_msg = s.req_state()
		curr_state = curr_state_msg[0]
		# curr_state = 1
		print (curr_state)

		print ('Got State variable :' + str(curr_state))

		#Act based on State
		if curr_state == 0:					# Server initialized
			print ("State is initialized. Standing by...")
			objList[3].visible = False
			objList[4].visible = False
			objList[5].visible = False

		elif curr_state == 1: 				# Step requested
		
			step_num = s.req_step_n()
			step_num[0] = 3 #Delete this[]
			s.update_state(2)
		
			print ("Rendering...")
		
			renderObject(step_num) #Call bge based function
		
			print ("Render complete.")
			s.update_state(3)
		
		elif curr_state == 2:				# Rendering...
			objList[3].visible = False
			objList[4].visible = False
			objList[5].visible = False
			print ("[Error] gem_blender_json: Why am I here?")
		
		elif curr_state == 3:				# Render complete, stand by
			objList[3].visible = False
			objList[4].visible = False
			objList[5].visible = False
			print ("Standing by...")
	

	Init()
	getState()