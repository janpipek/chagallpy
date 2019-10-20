from wowp.components import Actor

from .thumbnail_creator import ThumbnailCreator


class ArgumentParser(Actor):
    def __init__(self):
        super(ArgumentParser, self).__init__()
        self.inports.append("kwargs")
        self.outports.append("source_path")
        self.outports.append("output_path")
        self.outports.append("thumbnail_size")

    def get_run_args(self):
        kwargs = self.inports["kwargs"].pop()
        return (), kwargs

    SIZE = 256

    @classmethod
    def run(cls, *args, **kwargs):
        ThumbnailCreator.SIZE = cls.SIZE
        return {
            "source_path": kwargs["input"],
            "output_path": kwargs["output"],
            "thumbnail_size": cls.SIZE,
        }
