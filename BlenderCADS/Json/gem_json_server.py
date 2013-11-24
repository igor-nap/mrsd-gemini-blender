import jpc
import gem_graphics_engine

ge = gem_graphics_engine.Graphics_Engine()

# Data handling functions
class MyHandler(jpc.BaseHandler):
    def init (self,req_n):
        return ge.init(req_n)

    def req_state(self):
        return ge.req_state()

    def req_step_n(self):
        return ge.req_step_n()

    def render(self,req_n):
        return ge.render(req_n)

    def update_state(self,state):
        return ge.update_state(state)

print("Registering server...")
jpc.start_server(host='localhost', port=50000, handler=MyHandler)

