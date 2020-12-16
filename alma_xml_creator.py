"""
Create XML of multiple records that can be added to Alma via Import job.
"""

from xml.etree import ElementTree


class MarcCollection:
    """
    Create a collection of MARC21 records as xml.etree.ElementTree.Element
    """

    def __init__(self):
        """
        Initialize collection of records.
        """
        self.collection = self.create_collection_element()



    def append_record(self):
        record = ElementTree.SubElement(self.collection, 'record')
        return record

    @staticmethod
    def create_collection_element() -> ElementTree.Element:
        collection = ElementTree.Element('collection')
        return collection
