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

        def create_subfield(self, code: str, text: str):
            pass

        def append_datafield(self, attributes: tuple, subfields: tuple):
            datafield = ElementTree.SubElement(self.record, "datafield")
            datafield.set("tag", attributes[0])
            datafield.set("ind1", attributes[1])
            datafield.set("ind2", attributes[2])
            for subfield in subfields:
                datafield.append(subfield)
            return datafield

        def append_controlfield(self, tag: str, text: str):
            controlfield = self.append_field("controlfield", text)
            controlfield.set("tag", tag)
            return controlfield

        def append_leader(self, text: str):
            leader = self.append_field("leader", text)
            return leader

        def append_field(self, name, text):
            field = ElementTree.SubElement(self.record, name)
            field.text = text
            return field

    @staticmethod
    def create_collection_element() -> ElementTree.Element:
        collection = ElementTree.Element('collection')
        return collection
