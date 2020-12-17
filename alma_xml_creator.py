"""
Create XML of multiple records that can be added to Alma via Import job.
"""

from xml.etree import ElementTree
from xml.etree.ElementTree import Element


class MarcCollection:
    """
    Create a collection of MARC21 records as xml.etree.ElementTree.Element
    """
    def __init__(self):
        """
        Initialize collection of records.
        """
        self.collection = self.create_collection_element()

    class MarcRecord:
        """
        Create a single MARC21 record as xml.etree.ElementTree.Element
        """
        def __init__(self):
            self.record = ElementTree.Element('record')

    @staticmethod
    def create_collection_element() -> ElementTree.Element:
        collection = ElementTree.Element('collection')
        return collection
