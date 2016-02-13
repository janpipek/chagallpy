from wowp.components import Actor
import PIL
import PIL.ExifTags


class ExifDataReader(Actor):
    def __init__(self):
        super(ExifDataReader, self).__init__("EXIF data reader")
        self.inports.append("image_in")
        self.outports.append("image_out")

    def get_run_args(self):
        image_info = self.inports["image_in"].pop()
        return (image_info, ), {}

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
        except:
            pass
        return {"image_out" : image_info}

