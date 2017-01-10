import os
import datetime


class ExifProxy(object):
    """Object accessing EXIF info in a friendly, @property-friendly way.

    TODO: Work in progress
    """
    def __init__(self, a_dict):
        self._data = a_dict

    @property
    def camera(self):
        return self._data["Model"]


class ImageInfo(object):
    """Container for image information.

    Objects of this class are passed in the workflow.
    """
    def __init__(self, path):
        self.path = path
        self._exif_data = {}
        self.exif = None
        self._meta_data = {}
        self.previous = None
        self.next = None
        self.gallery_info = None

        self.index = 0
        self.total_count = 0

    @property
    def title(self):
        if "title" in self.meta_data:
            return self.meta_data["title"]
        else:
            return self.basename


    @property
    def basename(self):
        return os.path.splitext(os.path.basename(self.path))[0].lower()

    @property
    def exif_data(self):
        """Original EXIF data.

        :rtype: dict
        """
        return self._exif_data

    @exif_data.setter
    def exif_data(self, value):
        self._exif_data = value
        self.exif = ExifProxy(self._exif_data)

    @property
    def meta_data(self):
        return self._meta_data

    @meta_data.setter
    def meta_data(self, value):
        self._meta_data = value

    @property
    def date_time(self):
        """Best available data time info.

        :rtype datetime.datetime
        """
        if "date" in self.meta_data:
            return datetime.datetime.strptime(self.meta_data["date"], "%d/%m/%Y")
        if "DateTimeOriginal" in self._exif_data:
            exiftime = self._exif_data["DateTimeOriginal"]
            if not isinstance(exiftime, str):
                exiftime = exiftime[0]
            return datetime.datetime.strptime(exiftime, "%Y:%m:%d %H:%M:%S")
        if "DateTime" in self._exif_data:
            exiftime = self._exif_data["DateTime"]
            return datetime.datetime.strptime(exiftime, "%Y:%m:%d %H:%M:%S")
        ctime = int(os.path.getctime(self.path))
        return datetime.datetime.fromtimestamp(ctime)

    @property
    def place(self):
        return self.meta_data.get("place", None)

    @property
    def exif_orientation(self):
        if "Orientation" in self.exif_data:
            return self.exif_data["Orientation"]
        else:
            return 0

    def __repr__(self):
        return ("ImageInfo('{0}')".format(self.path))
