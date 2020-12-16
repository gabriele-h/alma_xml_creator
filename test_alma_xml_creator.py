"""
Tests for XML creation
"""

import pytest
from xml.etree import ElementTree

from alma_xml_creator import MarcCollection


class TestMarcCollection:
    """
    Does an instance of MarcCollection work as expected?
    """

    TestCollection = MarcCollection()
    collection = TestCollection.collection
    record = TestCollection.append_record()

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
