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

    output_path = "./build"

    # Get relevant images
    source = ImageCollector()

    # Read all data about them & make thumbnails
    data_chain = Chain.create_prototype("chain", [ExifDataReader, MetaDataReader, ThumbnailCreator(output_path)])
    data_map = Map(data_chain)
    data_map.inports["inp"] += source.outports["images"]

    # Correct order
    sorter = ImageSorter()
    sorter.inports["images_in"] += data_map.outports["out"]

    workflow = source.get_workflow()
    images = workflow(path=".")