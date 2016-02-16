from wowp.components import Actor


class ImageSorter(Actor):
    def __init__(self):
        super(ImageSorter, self).__init__()
        self.inports.append("images_in")
        self.outports.append("images_out")

    def get_run_args(self):
        args = tuple(port.pop() for port in self.inports)
        return args, {}

    @classmethod
    def run(cls, *args, **kwargs):
        images = args[0]
        images = sorted(images, key=lambda i: i.date_time)
        for index, image in enumerate(images):
            if len(images) > 1:
                if index > 0:
                    image.previous = images[index - 1]
                if index < len(images) - 1:
                    image.next = images[index + 1]
            image.total_count = len(images)
            image.index = index + 1
        return {"images_out" : images}

