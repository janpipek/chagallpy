# chagallpy

(Cha)rming (gall)ery in (Py)thon is a static, minimalistic and mostly JS-free web gallery generator.
In a way, it serves as an example project for the WOWP framework (see <http://pythonic.eu/wowp>).

The gallery does not depend on any external JS library and is navigable using
standard (whatever reasonable definition of "standard") keyboard shortcuts.

## Usage

Just run this command in the directory with photos:

```
chagall
```

It finds all JPEG images in the current directory, then tries to read metadata about them
and produces a gallery in subdirectory "build".

Example galleries produced with chagallpy: <http://i.vzdusne.cz/>

## Installation

Easiest way is to use "pip" and download the package from PyPI.

```
pip install chagallpy
```

Or, you can visit the GitHub page of the project and work with the development version:

<https://github.com/janpipek/chagallpy>

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
