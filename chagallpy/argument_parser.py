from wowp.components import Actor


class ArgumentParser(Actor):
    def __init__(self):
        super(ArgumentParser, self).__init__()
        self.inports.append("argv")
        self.outports.append("source_path")
        self.outports.append("output_path")

    def get_run_args(self):
        return tuple(self.inports["argv"].pop()), {}

    @classmethod
    def run(cls, *args, **kwargs):
        return {
            "source_path": ".",
            "output_path": "./build"
        }