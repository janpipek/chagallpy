import logging
import os
import re
from typing import List, Tuple, Any, Dict

from wowp.components import Actor

from .image_info import ImageInfo


class ImageCollector(Actor):
    """Actor that finds all JPEG images in a directory."""
    def __init__(self):
        super(ImageCollector, self).__init__(name="ImageCollector")
        self.inports.append("path")
        self.outports.append("images")

    def get_run_args(self):
        return (self.inports["path"].pop(),), {}

    @classmethod
    def run(cls, *args, **kwargs) :
        path = args[0]
        files = reglob(path, r".*\.[Jj][Pp][Ee]?[Gg]$")
        images = [ImageInfo(f) for f in files]
        logging.info(f"Found {len(images)} images.")
        return {"images": images}


def reglob(path: str, exp: str, invert: bool = False) -> List[str]:
    """glob.glob() style searching which uses regex

    :param path: Directory where to look for files
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

    res = [os.path.join(path, x) for x in res]
    return res
