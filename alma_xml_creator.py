"""
Create XML of multiple records that can be added to Alma via Import job.
"""

from csv import reader
from logging import getLogger
from re import compile
from sys import argv
from typing import Iterator
from xml.etree.ElementTree import Element, SubElement


logger = getLogger("alma_xml_creator")


def create_collection_from_reader(current_reader: Iterator[dict]):
    """
    For a given csv-reader create and populate a collection with records.
    :param current_reader: csv.reader of a file
    :return: collection as an xml.etree.ElementTree.Element
    """

    csv_header = next(current_reader)

    NewCollection = MarcCollection()
    new_collection = NewCollection.root

    for row in current_reader:

        NewRecord = NewCollection.MarcRecord()

        for i in range(0, len(row)):

            field_key = csv_header[i]
            field_value = row[i]

            if field_key in ('LDR', 'leader') and field_value != "":
                NewRecord.append_leader(field_value)
            elif field_key[0] == "0" and field_key[1] == "0" and field_value != "":
                NewRecord.append_controlfield(field_key, field_value)
            elif compile(r'^[0-9]{3}[0-9A-z ]{2}$').match(field_key) and field_value != "":
                NewRecord.append_datafield(field_key, field_value)
            else:
                logger.error(f"""field_key '{field_key}' did not match expectations. Skipping.""")

        new_collection.append(NewRecord.root)
        print(NewRecord.root)

    return new_collection


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


# Make this work as a cli-script, too
if __name__ == "main":

    csv_path = argv[1]
    xml_path = argv[2]

    with open(csv_path, newline="") as csv_file:
        csv_reader = reader(csv_file, delimiter=";")
        collection = create_collection_from_reader(csv_reader)

        with open(xml_path, newline="") as xml_file:
            collection.write(xml_file)
