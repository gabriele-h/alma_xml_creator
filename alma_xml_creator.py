"""
Create XML of multiple records that can be added to Alma via Import job.
"""

from logging import getLogger
from re import compile
from typing import Iterator
from xml.etree.ElementTree import Element, SubElement


logger = getLogger("alma_xml_creator")

class MarcCollection:
    """
    Create a collection of MARC21 records as xml.etree.ElementTree.Element
    """
    def __init__(self):
        """
        Initialize collection of records.
        """
        self.root = Element('collection')

    class MarcRecord:
        """
        Create a single MARC21 record as xml.etree.ElementTree.Element
        """
        def __init__(self):
            self.root = Element('record')

        def append_datafield(self, attributes: str, subfields: str) -> SubElement:
            datafield = SubElement(self.root, "datafield")
            datafield.set("tag", attributes[0:3])
            datafield.set("ind1", attributes[3])
            datafield.set("ind2", attributes[4])

            for subfield in subfields.lstrip("$").split('$$'):

                code = subfield[0]
                content = subfield[1:]
                subfield_element = self.create_subfield(code, content)

                try:
                    datafield.append(subfield_element)
                except TypeError:
                    logger.error("Could not append subfield.")

            return datafield

        @staticmethod
        def create_subfield(code: str, text: str) -> Element:
            subfield = Element("subfield")
            subfield.set("code", code)
            subfield.text = text
            return subfield

        def append_controlfield(self, tag: str, text: str) -> SubElement:
            controlfield = self.append_field("controlfield", text)
            controlfield.set("tag", tag)
            return controlfield

        def append_leader(self, text: str) -> SubElement:
            leader = self.append_field("leader", text)
            return leader

        def append_field(self, name: str, text: str) -> SubElement:
            field = SubElement(self.root, name)
            field.text = text
            return field
