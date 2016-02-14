# chagallpy

(Cha)rming (gall)ery in (Py)thon is a static, minimalistic and mostly JS-free web gallery.
In a way, it serves as an example project for the WOWP framework (see <http://pythonic.eu/wowp>).

## Installation

Currently, you have to manually install this library:

```
git clone git@github.com:janpipek/chagallpy.git
cd chagallpy
pip install .
```

And if, which is quite probable, you don't have wowp installed, please follow wowp's documentation:
<http://pythonic.eu/wowp/>.

## Configuration

### Gallery metadata

Metadata are store in `gallery.yaml`. Currently available configuration options:

* title

### Image metadata

Available EXIF data are read.

For each `image.jpg`, a file `image.yaml` is read with the following options:

* title
* place
* date (dd/mm/YYYY)

## Usage

There is an executable called `chagall` that does all the job. Currently, it starts from
current directory and places everything in `build/` output directory.


