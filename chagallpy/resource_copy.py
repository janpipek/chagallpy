from wowp.components import Actor
import os
import shutil


class ResourceCopy(Actor):
    def __init__(self):
        super(ResourceCopy, self).__init__()
        self.inports.append("path_in")
        self.outports.append("path_out")

    def get_run_args(self):
        return (self.inports["path_in"].pop(), ), {}

    @classmethod
    def run(cls, *args, **kwargs):
        output_path = args[0]
        os.makedirs(output_path, exist_ok=True)
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
        files = os.listdir(resource_dir)
        print("Copying:", files)
        for f in files:
            in_path = os.path.join(resource_dir, f)
            print("Copying:", in_path, "to", output_path)
            shutil.copy(in_path, output_path)
        return {"path_out" : output_path}