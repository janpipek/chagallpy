from wowp.components import Actor
import yaml
import os
import codecs


class MetaDataReader(Actor):
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
            with codecs.open(yaml_path, "r", encoding="utf-8") as yaml_f:
                image_info.meta_data.update(yaml.load(yaml_f))
        return {"image_out": image_info}