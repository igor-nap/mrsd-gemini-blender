"""

# States
0 - Initialized
1 - Step requested
2 - Rendering...
3 - Render complete

"""	

import jpc

import time

print "Connecting to server..."

c = jpc.connect(host='localhost', port=50000)
s = jpc.Proxy(c)

print "Connected."

curr_step = 0

for j in range (0,1000):
	
	curr_state_msg = s.req_state()
	curr_state = curr_state_msg[0]
	#print "Requested render: " + str(j)

	if curr_state == 0:					# Server initialized
		print "State is initialized. Standing by..."
	elif curr_state == 1: 				# Step requested
		
		step_num = s.req_step_n()
		s.update_state(2)
		print "Rendering..."
		for i in range (0,30):
			time.sleep(0.1) # Simulate doing something 

		print "Render complete."
		s.update_state(3)
	elif curr_state == 2:				# Rendering...
		print "[Error] gem_blender_json: Why am I here?"
	elif curr_state == 3:				# Render complete, stand by
		print "Standing by..."

	time.sleep(0.1)
	#time.sleep(0.03)

print "Finished."
