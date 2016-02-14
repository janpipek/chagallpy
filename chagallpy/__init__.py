__version__ = str('0.1.0')

import sys


def generate():
    from wowp.actors.experimental import Chain
    from wowp.actors.mapreduce import Map

    from chagallpy.thumbnail_creator import ThumbnailCreator
    from chagallpy.image_sorter import ImageSorter
    from chagallpy.exif_data_reader import ExifDataReader
    from chagallpy.image_collector import ImageCollector
    from chagallpy.meta_data_reader import MetaDataReader
    from chagallpy.image_sorter import ImageSorter
    from chagallpy.album_page_creator import AlbumPageCreator
    from chagallpy.image_page_creator import ImagePageCreator
    from chagallpy.resource_copy import ResourceCopy

    output_path = "./build"

    # Do the initial setup
    resource_copy = ResourceCopy()
    resource_copy.get_workflow()(path_in=output_path)

    # Get relevant images
    source = ImageCollector()

    # Read all data about them & make thumbnails
    data_chain = Chain.create_prototype("chain", [ExifDataReader, MetaDataReader, ThumbnailCreator(output_path)])
    data_map = Map(data_chain)
    data_map.inports["inp"] += source.outports["images"]

    # Correct order
    sorter = ImageSorter()
    sorter.inports["images_in"] += data_map.outports["out"]

    # Create album page
    album_creator = AlbumPageCreator(output_path)
    album_creator.inports["images"] += sorter.outports["images_out"]

    # Create all image pages
    image_page_creator = ImagePageCreator.create_prototype(output_path)
    image_page_map = Map(image_page_creator)
    image_page_map.inports["inp"] += sorter.outports["images_out"]

    workflow = source.get_workflow()
    images = workflow(path=".")