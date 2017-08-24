from wowp.components import Actor
import os
import jinja2
import codecs


class GalleryPageCreator(Actor):
    def __init__(self, output_path):
        super(GalleryPageCreator, self).__init__()
        self.output_path = os.path.abspath(output_path)
        self.inports.append("images")
        self.inports.append("gallery_info")
        self.inports.append("output_path")
        self.inports.append("thumbnail_size")

    def get_run_args(self):
        args = (self.inports["images"].pop(), self.inports["gallery_info"].pop(), self.inports["thumbnail_size"].pop())
        kwargs = {"output_path": self.inports["output_path"].pop()}
        return args, kwargs

    @classmethod
    def run(cls, *args, **kwargs):
        images = args[0]
        gallery_info = args[1]
        thumbnail_size = args[2]
        outfile = os.path.join(kwargs.get("output_path"), "index.html")
        cls.create_page(images, gallery_info, outfile, thumbnail_size)
        return { }

    @classmethod
    def create_page(cls, images, gallery_info, outfile, thumbnail_size, **kwargs):
        basedir = os.path.dirname(os.path.abspath(__file__))

        jinja_loader = jinja2.FileSystemLoader(os.path.join(basedir, "templates"))
        env = jinja2.Environment(loader=jinja_loader)

        template = env.get_template("index.html")

        print("Creating album page index.html...")

        with codecs.open(outfile, "w", encoding="utf-8") as fout:
            fout.write(template.render(images=images, gallery=gallery_info, thumbnail_size=thumbnail_size))




