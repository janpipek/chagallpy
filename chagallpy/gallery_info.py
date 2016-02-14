

class GalleryInfo(object):
    def __init__(self, meta_data):
        self.meta_data = meta_data

    @property
    def title(self):
        if "title" in self.meta_data:
            return self.meta_data["title"]