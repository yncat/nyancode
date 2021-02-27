import nyancode_runtime_std


class Runner:
    def __init__(self, program, parent_window):
        self.program = program
        print(program)
        self.parent_window = parent_window

    def run(self):
        exec(self.program, {"nyancode": nyancode_runtime})
