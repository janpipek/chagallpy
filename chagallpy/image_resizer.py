from wowp.components import Actor
import os
from PIL import Image
import shutil


class ImageResizer(Actor):
    def __init__(self, output_path, max_height, max_width):
        super(ImageResizer, self).__init__()
        self.output_path = output_path
        self.inports.append("image_in")
        self.max_width = max_width
        self.max_height = max_height
        self.outports.append("out_file")

    def get_run_args(self):
        return (self.inports["image_in"].pop(),), {
            "output_path": self.output_path,
            "max_width": self.max_width,
            "max_height": self.max_height
        }

    @classmethod
    def run(cls, *args, **kwargs):
        image = args[0]
        max_width = kwargs.get("max_width")
        max_height = kwargs.get("max_height")
        infile = image.path
        filename = image.basename + ".jpg"
        outfile = os.path.join(kwargs.get("output_path"), filename)
        cls.resize_image(infile, outfile, max_width, max_height, orientation=image.exif_orientation)
        return {
            "out_file": outfile
        }

    @classmethod
    def resize_image(cls, infile, outfile, max_width=1600, max_height=1600, preserve_exif=True, orientation=1, **kwargs):
        if os.path.isfile(outfile):
            print("Not resizing image {0}...".format(outfile))
            return    # Unless forced
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        print("Resizing image {0}...".format(outfile))

        img = Image.open(infile)

        exif = None

        if preserve_exif:
            try:
                exif = img.info['exif']
            except KeyError:
                pass

        if orientation == 3:   img = img.transpose(Image.ROTATE_180)
        elif orientation == 6: img = img.transpose(Image.ROTATE_270)
        elif orientation == 8: img = img.transpose(Image.ROTATE_90)

        scale = 1.0
        if img.width > max_width:
            scale = max_width / img.width
        if img.height > max_height:
            scale = min(scale, max_height / img.height)

        if scale < 1.0:
            width = int(scale * img.width)
            height = int(scale * img.height)
            resized = img.resize((width, height), Image.BICUBIC)
            if exif:
                resized.save(outfile, exif=exif)
            else:
                resized.save(outfile)
        else:
            shutil.copy(infile, outfile)
