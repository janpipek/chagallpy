import logging

from wowp.components import Actor

from .thumbnail_creator import ThumbnailCreator


class ArgumentParser(Actor):
    """Actor that passes CLI arguments.

    The arguments need to be preprocessed by click.
    """
    def __init__(self):
        super(ArgumentParser, self).__init__()
        self.inports.append("kwargs")
        self.outports.append("source_path")
        self.outports.append("output_path")
        self.outports.append("thumbnail_size")
        self.outports.append("image_size")

    def get_run_args(self):
        kwargs = self.inports["kwargs"].pop()
        return (), kwargs

    SIZE = 256

    @classmethod
    def run(cls, *args, **kwargs):
        ThumbnailCreator.SIZE = cls.SIZE
        parsed_args = {
            "source_path": kwargs["input"],
            "output_path": kwargs["output"],
            "thumbnail_size": kwargs["thumbnail_size"],
            "image_size": kwargs["image_size"],
        }
        logging.debug(f"Running with arguments: {parsed_args}")
        return parsed_args
