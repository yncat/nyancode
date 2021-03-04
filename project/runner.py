import os
import nyancode_runtime_std as nyancode_runtime
import constants


class Runner:
    def __init__(self, program, parent_window):
        self.program = program
        self.parent_window = parent_window

    def run(self):
        nyancode_runtime.configure(
            parent_window=self.parent_window,
            data_directory=constants.DATA_DIRECTORY
        )
        exec(self.program, {"nyancode": nyancode_runtime})
