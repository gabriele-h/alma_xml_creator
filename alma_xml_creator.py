"""
Create XML of multiple records that can be added to Alma via Import job.
"""

from xml.etree import ElementTree


def create_collection_element() -> ElementTree.Element:
    collection = ElementTree.Element('collection')
    return collection


def append_record(collection: ElementTree.Element):
    record = ElementTree.SubElement(collection, 'record')
    return record
