class GalleryInfo:
    """Meta-data about a gallery."""
    def __init__(self, meta_data: dict):
        self.meta_data = meta_data

    @property
    def title(self) -> str:
        if "title" in self.meta_data:
            return self.meta_data["title"]
