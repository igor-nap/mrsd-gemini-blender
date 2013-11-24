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

init_state = 0

print "Initializing..."
s.init(0)
state_n = 0

for j in range (0,100):
	
	#s.render(j)
	#print "Requested render: " + str(j)

	for i in range (0,30):
		curr_state_msg = s.req_state()
		curr_state = curr_state_msg[0]
		print "Current state: " + str(curr_state)
		time.sleep(0.1)
		#time.sleep(0.03)

		if curr_state == 0:					# Server initialized, send render
			print "State is initialized. Sending render request..."
			state_n = state_n + 1
			s.render(state_n)
			print "Requested step: " + str(state_n)

		elif curr_state == 1: 				# Step requested
			print "Step requested. Standing by ... "

		elif curr_state == 2:				# Rendering...
			print "Rendering..."

		elif curr_state == 3:				# Render complete, stand by
			print "Render complete. Retrieving image file..."
			time.sleep(2)
			print "Image retrieved. Sending new render request..."
			state_n = state_n + 1
			s.render(state_n)
			print "Requested step: " + str(state_n)

print "Finished."
