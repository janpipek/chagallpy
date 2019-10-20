import logging

import PIL
import PIL.ExifTags

from wowp.components import Actor


class ExifDataReader(Actor):
    """Actor reading EXIF data for an image."""
    def __init__(self):
        super(ExifDataReader, self).__init__("EXIF data reader")
        self.inports.append("image_in")
        self.outports.append("image_out")

    def get_run_args(self):
        image_info = self.inports["image_in"].pop()
        return (image_info,), {}

    @classmethod
    def run(cls, *args, **kwargs):
        image_info = args[0]
        try:
            img = PIL.Image.open(image_info.path)
            image_info.exif_data = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
            logging.debug(f"Reading EXIF data for image {image_info.path}")
        except Exception:
            logging.debug(f"EXIF data not found for image {image_info.path}")
        return {"image_out": image_info}
