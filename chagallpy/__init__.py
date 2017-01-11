__version__ = str('0.1.3')

import sys


def generate():
    from wowp.actors.experimental import Chain
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

    output_path = "./build"    # TODO: remove

    # Do the initial setup
    resource_copy = ResourceCopy()
    resource_copy.inports["path_in"] += parser.outports["output_path"]

    # Get relevant images
    source = ImageCollector()
    source.inports["path"] += parser.outports["source_path"]

    # Read all data about them & make thumbnails
    data_chain = ConstructorWrapper(Chain, "chain", [ExifDataReader, MetaDataReader])
    data_map = Map(data_chain)
    data_map.inports["inp"] += source.outports["images"]

    # Correct order
    sorter = ImageSorter()
    sorter.inports["images_in"] += data_map.outports["out"]

    # Get general gallery information
    gallery_info_reader = GalleryInfoReader()
    gallery_info_reader.inports["images_in"] += sorter.outports["images_out"]
    gallery_info_reader.inports["path_in"] += parser.outports["source_path"]

    # Create album page
    gallery_creator = GalleryPageCreator(output_path)
    gallery_creator.inports["images"] += gallery_info_reader.outports["images_out"]
    gallery_creator.inports["gallery_info"] += gallery_info_reader.outports["gallery_info"]
    gallery_creator.inports["output_path"] += parser.outports["output_path"]

    # Copy & resize all images
    image_resizer = ConstructorWrapper(ImageResizer, output_path=output_path, max_height=1600, max_width=1600)
    image_thumbnailer = ConstructorWrapper(ThumbnailCreator, output_path=output_path)
    image_resizer_chain = ConstructorWrapper(Chain, "image_resizer_chain", [image_resizer, image_thumbnailer])
    image_resizer_map = Map(image_resizer_chain)
    image_resizer_map.inports["inp"] += gallery_info_reader.outports["images_out"]

    # Create all image pages
    image_page_creator = ConstructorWrapper(ImagePageCreator, output_path)
    image_page_map = Map(image_page_creator)
    image_page_map.inports["inp"] += gallery_info_reader.outports["images_out"]

    workflow = parser.get_workflow()
    images = workflow(argv=sys.argv)
