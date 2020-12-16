"""
Tests for XML creation
"""

import pytest
from xml.etree.ElementTree import Element

import alma_xml_creator


class TestCreateCollectionTree:

    collection = alma_xml_creator.create_collection_tree()

    def test_is_element(self):
        """create_collection_tree() should return an Element"""
        assert type(self.collection) == Element
