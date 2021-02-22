import nyancode_runtime

class Runner:
    def __init__(self, program, parent_window):
        self.program=program
        self.parent_window = parent_window
    def run():
        exec(self.program, {"nyancode": nyancode_runtime})


      