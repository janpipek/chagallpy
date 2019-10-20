import codecs
import os

import jinja2

from wowp.components import Actor


class ImagePageCreator(Actor):
    def __init__(self):
        super(ImagePageCreator, self).__init__()
        self.inports.append("image_in")
        self.inports.append("output_path")
        self.outports.append("image_out")

    def get_run_args(self):
        args = (self.inports["image_in"].pop(),)
        kwargs = {"output_path": self.inports["output_path"].pop()}
        return args, kwargs

    @classmethod
    def run(cls, *args, **kwargs):
        image = args[0]
        output_path = kwargs.get("output_path")
        outfile = os.path.join(output_path, image.basename + ".html")
        cls.create_page(image, outfile)
        return {"image_out": image}

    @classmethod
    def create_page(cls, image, outfile, **kwargs):
        print("Creating image page {0}...".format(outfile))
        basedir = os.path.dirname(os.path.abspath(__file__))

        jinja_loader = jinja2.FileSystemLoader(os.path.join(basedir, "templates"))
        env = jinja2.Environment(loader=jinja_loader)

        template = env.get_template("image_page.html")

        with codecs.open(outfile, "w", encoding="utf-8") as fout:
            fout.write(template.render(image=image))
