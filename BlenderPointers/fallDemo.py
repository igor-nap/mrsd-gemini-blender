import jpc
import time
from bge import logic
from bge import events
import mathutils

stepFile = open('/home/bhala/DevTools/mrsd-gemini/BlenderPointers/gemini_steps1.txt')
logic.LibLoad("/home/bhala/DevTools/mrsd-gemini/BlenderPointers/animateObjects.blend","Mesh")

meshCount = 0
step_num = -1

#List of STL Files stored according to the step IDs"
meshList = ['arrowFlat','circleArrow','crossHair']
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


# Set Initial Camera View to Top View
scene = logic.getCurrentScene() 
cam = scene.active_camera 

camPose = mathutils.Euler((0,0,0),'XYZ') 
cam.worldPosition = [0, 0, 20]
cam.worldOrientation = camPose

print ('Connecting to Server..')
c = jpc.connect(host = 'localhost',port=50000)
s = jpc.Proxy(c)
print ('Connected')
print(animateIndex)

def renderStep():
	cubeController = logic.getCurrentController()
	cubeOwn = cubeController.owner


	def Init():
		if not 'init' in cubeOwn:
			cubeOwn['init'] =1 

	#Load the meshes corresponding to the step_num		
	def renderObject(step_num):
		scene = logic.getCurrentScene()
		cube = scene.objects['Cube']

		pointInd = animateIndex[step_num[0]]
		print(pointInd)

		mesh = meshList[animateIndex[step_num[0]]]
		cube.replaceMesh(mesh)
		cube.localScale.x = 0.03
		cube.localScale.z = 0.03
		cube.localScale.y = 0.03
		# cube.localPosition.y  = -2
		# cube.localPosition.x  = -2


	#Get the state from JSON Server
	def getState():

		global meshList,meshCount
		global step_num, s

		curr_state_msg = s.req_state()
		# curr_state = curr_state_msg[0]
		curr_state = 1
		# print (curr_state)

		print ('State variable got :' + str(curr_state))

		#Act based on State
		if curr_state == 0:					# Server initialized
			print ("State is initialized. Standing by...")
		elif curr_state == 1: 				# Step requested
		
			step_num = s.req_step_n()
			step_num[0] = 2
			 #Delete this[]
			s.update_state(2)
		
			print ("Rendering...")
		
			renderObject(step_num) #Call bge based function
		
			print ("Render complete.")
			s.update_state(3)
		
		elif curr_state == 2:				# Rendering...
			print ("[Error] gem_blender_json: Why am I here?")
		elif curr_state == 3:				# Render complete, stand by
			print ("Standing by...")
	

	Init()
	getState()