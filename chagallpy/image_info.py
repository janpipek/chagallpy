import os
import datetime


class ImageInfo(object):
    """Container for image information.

    Objects of this class are passed in the workflow.
    """
    def __init__(self, path):
        self.path = path
        self._exif_data = {}
        self._meta_data = {}
        self.previous = None
        self.next = None

    @property
    def exif_data(self):
        return self._exif_data

    @exif_data.setter
    def exif_data(self, value):
        self._exif_data = value

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
        if "DateTime" in self._exif_data:
            exiftime = self._exif_data["DateTime"]
            return datetime.datetime.strptime(exiftime, "%Y:%m:%d %H:%M:%S")
        ctime = int(os.path.getctime(self.path))
        return datetime.datetime.fromtimestamp(ctime)

    def __repr__(self):
        return ("ImageInfo('{0}')".format(self.path))
