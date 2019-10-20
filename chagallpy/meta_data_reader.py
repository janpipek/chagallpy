import codecs
import logging
import os

import yaml

from wowp.components import Actor


class MetaDataReader(Actor):
    """Actor reading associated meta-data for images."""
    def __init__(self):
        super(MetaDataReader, self).__init__(name="MetaDataReader")
        self.inports.append("image_in")
        self.outports.append("image_out")

    def get_run_args(self):
        return (self.inports["image_in"].pop(),), {}

    @classmethod
    def run(cls, *args, **kwargs):
        image_info = args[0]
        yaml_path = os.path.splitext(image_info.path)[0] + ".yaml"
        if os.path.isfile(yaml_path):
            logging.debug(f"Reading meta data for {image_info.path}...")
            with codecs.open(yaml_path, "r", encoding="utf-8") as yaml_f:
                image_info.meta_data.update(yaml.load(yaml_f, Loader=yaml.FullLoader))
        else:
            logging.debug(f"No meta data for {image_info.path}.")
        return {"image_out": image_info}
