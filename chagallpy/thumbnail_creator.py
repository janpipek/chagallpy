import logging
import os

from PIL import Image

from wowp.components import Actor


class ThumbnailCreator(Actor):
    def __init__(self):
        super(ThumbnailCreator, self).__init__(name="Thumbnail creator")
        self.inports.append("infile")
        self.inports.append("thumbnail_size")
        self.outports.append("outfile")

    def get_run_args(self):
        args = (self.inports["infile"].pop(), self.inports["thumbnail_size"].pop())
        kwargs = {}
        return args, kwargs

    @classmethod
    def run(cls, *args, **kwargs):
        infile = args[0]
        size = args[1]
        outfile = os.path.splitext(infile)[0] + ".thumb.jpg"
        cls.create_thumbnail(infile, outfile, size=size)
        return {"outfile": outfile}

    @classmethod
    def create_thumbnail(cls, infile, outfile, *, size):
        if os.path.isfile(outfile):
            logging.debug("Not creating thumbnail {0}...".format(outfile))
            return  # Unless forced
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        logging.debug("Creating thumbnail {0}...".format(outfile))

        img = Image.open(infile)

        ratio = float(size) / min(img.width, img.height)
        width = max(int(img.width * ratio), size)
        height = max(int(img.height * ratio), size)
        left = int((width - size) / 2)
        top = int((height - size) / 2)
        img = img.resize((width, height), Image.ANTIALIAS)
        img = img.crop((left, top, left + size, top + size))
        img.save(outfile)
