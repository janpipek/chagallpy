from wowp.components import Actor
import os
import re
from .image_info import ImageInfo


class ImageCollector(Actor):
    def __init__(self):
        super(ImageCollector, self).__init__(name="ImageCollector")
        self.inports.append("path")
        self.outports.append("images")

    def get_run_args(self):
        return (self.inports["path"].pop(), ), {}

    @classmethod
    def run(cls, *args, **kwargs):
        path = args[0]
        files = reglob(path, ".*\.[Jj][Pp][Ee]?[Gg]$")
        images = [ImageInfo(f) for f in files]
        return {"images" : images}


def reglob(path, exp, invert=False):
    """glob.glob() style searching which uses regex

    :param exp: Regex expression for filename
    :param invert: Invert match to non matching files

    Inspiration from:
        http://stackoverflow.com/questions/13031989/regular-expression-using-in-glob-glob-of-python
    """

    m = re.compile(exp)

    if invert is False:
        res = [f for f in os.listdir(path) if m.match(f)]
    else:
        res = [f for f in os.listdir(path) if not m.match(f)]

    res = map(lambda x: os.path.join(path, x), res)
    return res
