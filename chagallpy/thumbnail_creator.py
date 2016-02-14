from wowp.components import Actor
import os
from PIL import Image


class ThumbnailCreator(Actor):
    SIZE = 256

    def __init__(self, output_path):
        super(ThumbnailCreator, self).__init__(name="Thumbnail creator")
        self.output_path = os.path.abspath(output_path)
        self.inports.append("image_in")
        self.outports.append("image_out")

    def get_run_args(self):
        args = (self.inports["image_in"].pop(),)
        kwargs = {"output_path": self.output_path}
        return args, kwargs

    @classmethod
    def run(cls, *args, **kwargs):
        image = args[0]
        infile = image.path
        filename = image.basename + ".thumb.jpg"
        outfile = os.path.join(kwargs.get("output_path"), filename)
        cls.create_thumbnail(infile, outfile)
        return {
            "image_out": image
        }

    @classmethod
    def create_thumbnail(cls, infile, outfile, **kwargs):
        if os.path.isfile(outfile):
            return    # Unless forced
        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        size = kwargs.get("size", cls.SIZE)
        img = Image.open(infile)

        ratio = float(size) / min(img.width, img.height)
        width = max(int(img.width * ratio), size)
        height = max(int(img.height * ratio), size)
        left = int((width - size) / 2)
        top = int((height - size) / 2)
        img = img.resize((width, height), Image.ANTIALIAS)
        img = img.crop((left, top, left + size, top + size))
        img.save(outfile)

