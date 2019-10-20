import logging
import os
import warnings

import click


__version__ = str("0.1.5")


@click.command()
@click.option("--input", "-i", default=".")
@click.option("--output", "-o", default=os.path.join(".", "build"))
@click.option("--image-size", "-S", type=int, default=1600)
@click.option("--thumbnail-size", "-T", type=int, default=256)
@click.option("--verbose", "-v", count=True)
# @click.option("--static-path", type=str, default=None)
def generate(verbose, **kwargs):
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    elif verbose == 2:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    warnings.filterwarnings("ignore")

    from wowp.actors.special import Chain
    from wowp.actors.mapreduce import Map
    from wowp.util import ConstructorWrapper

    from chagallpy.thumbnail_creator import ThumbnailCreator
    from chagallpy.image_sorter import ImageSorter
    from chagallpy.exif_data_reader import ExifDataReader
    from chagallpy.image_collector import ImageCollector
    from chagallpy.meta_data_reader import MetaDataReader
    from chagallpy.image_sorter import ImageSorter
    from chagallpy.gallery_page_creator import GalleryPageCreator
    from chagallpy.image_page_creator import ImagePageCreator
    from chagallpy.resource_copy import ResourceCopy
    from chagallpy.gallery_info_reader import GalleryInfoReader
    from chagallpy.argument_parser import ArgumentParser
    from chagallpy.image_resizer import ImageResizer

    parser = ArgumentParser()

    # Do the initial setup
    resource_copy = ResourceCopy()
    resource_copy.inports["path_in"] += parser.outports["output_path"]

    # Get relevant images
    source = ImageCollector()
    source.inports["path"] += parser.outports["source_path"]

    # Read all data about them & make thumbnails
    data_chain = ConstructorWrapper(Chain, "chain", [ExifDataReader, MetaDataReader])
    data_map = Map(data_chain)
    data_map.inports["image_in"] += source.outports["images"]

    # Correct order
    sorter = ImageSorter()
    sorter.inports["images_in"] += data_map.outports["image_out"]

    # Get general gallery information
    gallery_info_reader = GalleryInfoReader()
    gallery_info_reader.inports["images_in"] += sorter.outports["images_out"]
    gallery_info_reader.inports["path_in"] += parser.outports["source_path"]

    # Create album page
    gallery_creator = GalleryPageCreator()
    gallery_creator.inports["images"] += gallery_info_reader.outports["images_out"]
    gallery_creator.inports["gallery_info"] += gallery_info_reader.outports[
        "gallery_info"
    ]
    gallery_creator.inports["output_path"] += parser.outports["output_path"]
    gallery_creator.inports["thumbnail_size"] += parser.outports["thumbnail_size"]

    # Copy & resize all images
    image_resizer_map = Map(ConstructorWrapper(ImageResizer), single_value_ports=("output_path", "image_size"))
    image_resizer_map.inports["image_in"] += sorter.outports["images_out"]
    image_resizer_map.inports["image_size"] += parser.outports["image_size"]
    image_resizer_map.inports["output_path"] += parser.outports["output_path"]

    # Make thumbnail from resized images
    image_thumbnailer_map = Map(ConstructorWrapper(ThumbnailCreator), single_value_ports=("thumbnail_size",))
    image_thumbnailer_map.inports["thumbnail_size"] += parser.outports["thumbnail_size"]
    image_thumbnailer_map.inports["infile"] += image_resizer_map.outports["out_file"]

    # Create all image pages
    image_page_creator = ConstructorWrapper(ImagePageCreator)
    image_page_map = Map(image_page_creator, single_value_ports=("output_path",))
    image_page_map.inports["image_in"] += gallery_info_reader.outports["images_out"]
    image_page_map.inports["output_path"] += parser.outports["output_path"]

    workflow = parser.get_workflow()
    images = workflow(kwargs=kwargs)


if __name__ == "__main__":
    generate()
