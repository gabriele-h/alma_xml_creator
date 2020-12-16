"""
Create XML of multiple records that can be added to Alma via Import job.
"""

from xml.etree import ElementTree


def create_collection_tree() -> ElementTree.Element:
    collection = ElementTree.Element('collection')
    return collection
