import datetime
import os
import re
from typing import Optional


class ExifProxy:
    """Object accessing EXIF info in a friendly, @property-friendly way.

    All properties are user-friendly strings
    """

    def __init__(self, a_dict):
        self._data = a_dict

    @property
    def camera(self) -> str:
        model = self._data.get("Model")
        if model:
            # Note: the selection of models is a little bit arbitrary...
            if model == "6039Y":
                model = "Alcatel Idol 3"
            elif model == "GT-N8010":
                model = "Samsung Galaxy Note 10.1"
            elif model == "GT-I8150":
                model = "Samsung Galaxy W"
            elif model.startswith("DiMAGE"):
                model = "Konica " + model
            elif model == "C4100Z,C4000Z":
                model = "Olympus C4000Z"
            elif model.startswith("Canon EOS"):
                model = model.replace(" DIGITAL", "")
            else:
                model = model.replace("NIKON", "Nikon")
        return model

    @property
    def iso(self) -> str:
        return self._data.get("ISOSpeedRatings")

    @property
    def aperture(self) -> Optional[str]:
        values = self._data.get("ApertureValue") or self._data.get("FNumber")
        if values:
            return "f/{0:.1f}".format(values[0] / values[1])
        else:
            return None

    @property
    def exposure(self) -> Optional[str]:
        values = self._data.get("ExposureTime")
        if values:
            value = values[0] / values[1]
            if value < 0.02:
                return "1/{0} s".format(int(1 / value))
            elif value < 0.1:
                return "1/{0:.1f} s".format(1 / value)
            elif value < 10:
                return "{0:.1f} s".format(value)
            else:
                return "{0} s".format(int(value))

        else:
            return None

    @property
    def crop_factor(self) -> Optional[float]:
        if "PowerShot G16" in self.camera:
            return 4.598
        elif self.camera == "Alcatel Idol 3":
            return 7.38
        elif re.match("Canon EOS \\d\\d\\d?D", self.camera):
            return 1.6
        elif re.match("Nikon D\\d0", self.camera):
            return 1.5
        elif re.search("Canon EOS 6D", self.camera):
            return 1.0
        elif self.camera == "Olympus C4000Z":
            return 5
        elif "Nexus 5X" in self.camera:
            return 5.49
        else:
            return None

    @property
    def focal_length(self):
        values = self._data.get("FocalLength")
        if values:
            value = values[0] / values[1]
            if self.crop_factor and self.crop_factor != 1.0:
                return "{0:.1f} (~{1:.1f}) mm".format(value, value * self.crop_factor)
            else:
                return "{0:.1f} mm".format(value)
        else:
            return None


class ImageInfo:
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

    def has_title(self) -> bool:
        return bool(self.meta_data.get("title"))

    @property
    def title(self) -> str:
        title = self.meta_data.get("title")
        if not title:
            return "[untitled]"
        else:
            return title

    @property
    def basename(self) -> str:
        return os.path.splitext(os.path.basename(self.path))[0].lower()

    @property
    def exif_data(self) -> dict:
        """Original EXIF data."""
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
    def date_time(self) -> datetime.datetime:
        """Best available data time info."""
        if "datetime" in self.meta_data:
            try:
                return datetime.datetime.strptime(
                    self.meta_data["datetime"], "%d/%m/%Y %H:%M:%S"
                )
            except ValueError:
                return datetime.datetime.strptime(
                    self.meta_data["datetime"], "%d/%m/%Y %H:%M"
                )
        elif "date" in self.meta_data:
            return datetime.datetime.strptime(self.meta_data["date"], "%d/%m/%Y")
        elif "DateTimeOriginal" in self._exif_data:
            exiftime = self._exif_data["DateTimeOriginal"]
            if not isinstance(exiftime, str):
                exiftime = exiftime[0]
            return datetime.datetime.strptime(exiftime, "%Y:%m:%d %H:%M:%S")
        elif "DateTime" in self._exif_data:
            exiftime = self._exif_data["DateTime"]
            return datetime.datetime.strptime(exiftime, "%Y:%m:%d %H:%M:%S")
        else:
            ctime = int(os.path.getctime(self.path))
            return datetime.datetime.fromtimestamp(ctime)

    @property
    def author(self) -> Optional[str]:
        return self.meta_data.get("author", None)

    @property
    def place(self) -> Optional[str]:
        return self.meta_data.get("place", None)

    @property
    def exif_orientation(self):
        if "Orientation" in self.exif_data:
            return self.exif_data["Orientation"]
        else:
            return 0

    def __repr__(self):
        return "ImageInfo('{0}')".format(self.path)
