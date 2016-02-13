from wowp.components import Actor


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
        image_info.meta_data = {"processed": True}
        # ... Do the thing
        return {"image_out": image_info}