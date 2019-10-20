import codecs
import logging
import os

import yaml

from wowp.components import Actor

from .gallery_info import GalleryInfo


class GalleryInfoReader(Actor):
    """Actor reading meta-data about gallery."""
    def __init__(self):
        super(GalleryInfoReader, self).__init__()
        self.inports.append("path_in")
        self.inports.append("images_in")
        self.outports.append("images_out")
        self.outports.append("gallery_info")

    def get_run_args(self):
        return (self.inports["path_in"].pop(), self.inports["images_in"].pop()), {}

    @classmethod
    def run(cls, *args, **kwargs):
        path = args[0]
        image_infos = args[1]
        yaml_path = os.path.join(path, "gallery.yaml")
        logging.debug(f"Reading gallery info from {yaml_path}...")
        meta_data = {}
        if os.path.isfile(yaml_path):
            with codecs.open(yaml_path, "r", encoding="utf-8") as yaml_f:
                meta_data.update(yaml.load(yaml_f, Loader=yaml.FullLoader))
        gallery_info = GalleryInfo(meta_data)
        # TODO: Move this from here to the DAG
        for image_info in image_infos:
            image_info.gallery_info = gallery_info
        return {"gallery_info": gallery_info, "images_out": image_infos}
