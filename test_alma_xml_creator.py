"""
Tests for XML creation
"""

import pytest
from xml.etree import ElementTree

import alma_xml_creator


class TestCreateCollection:

    collection = alma_xml_creator.create_collection_element()
    record = alma_xml_creator.append_record(collection)

    def test_can_add_subelement(self):
        """Output from create_collection_tree() can have SubElement"""
        testelement = ElementTree.SubElement(self.collection, "testelement")
        assert testelement.tag == "testelement"

    def test_append_record(self):
        """Appending a record works"""
        assert self.record.tag == "record"

    def test_collection_has_record(self):
        """Is the record actually appended to the collection?"""
        records = self.collection.findall('record')
        assert len(records) > 0
