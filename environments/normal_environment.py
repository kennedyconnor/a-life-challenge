from environments import Environment

class NormalEnvironment(Environment):
    def __init__(self):
        super().__init__('Normal',0.008, 0.02, 0.04,
                         1.0, "grey")