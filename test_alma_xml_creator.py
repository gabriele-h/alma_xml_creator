"""
Tests for XML creation
"""

import pytest
from xml.etree import ElementTree

import alma_xml_creator


class TestCreateCollectionTree:

    collection = alma_xml_creator.create_collection_tree()

    def test_can_add_subelement(self):
        """Output from create_collection_tree() can have SubElement"""
        testelement = ElementTree.SubElement(self.collection, "testelement")
        assert testelement.tag == "testelement"
