"""

# States
0 - Initialized
1 - Step requested
2 - Rendering...
3 - Render complete

"""


class Graphics_Engine:
    def __init__(self):
        self.state = 0
        self.step_n = 0
        self.req_n = 0

    def init(self,n):
        self.state = 0
        self.step_n = 0
        self.req_n = n
        return 1

    def req_state(self):
        curr_status = []
        curr_status.append(self.state)
        return curr_status

    def req_step_n(self):
        curr_status = []
        curr_status.append(self.step_n)
        return curr_status

    def render(self,req_n):
        self.req_n = req_n
        self.state = 1
        return 1

    def update_state(self,state):
        self.state = state
        self.step_n = self.req_n
        return 1
