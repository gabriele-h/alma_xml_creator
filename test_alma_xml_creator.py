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
    collection = TestCollection.root
    TestRecord = TestCollection.MarcRecord()
    record = TestRecord.root
    leader = TestRecord.append_leader('     ntm a22      c 4500')
    controlfield = TestRecord.append_controlfield('007', 'tu')
    subfields = (
        TestRecord.create_subfield("a", "ger"),
        TestRecord.create_subfield("c", "eng")
    )
    datafield = TestRecord.append_datafield(('041', ' ', '1'), subfields)

    def test_collection_has_tag(self):
        """Creating the colleciton worked"""
        assert self.collection.tag == "collection"

    def test_can_add_subelement(self):
        """Output from create_collection_tree() can have SubElement"""
        testelement = ElementTree.SubElement(self.collection, "testelement")
        assert testelement.tag == "testelement"

    def test_record_has_tag(self):
        """Creating the record worked"""
        assert self.record.tag == "record"

    def test_collection_has_record(self):
        """Can the record be appended to the collection?"""
        self.collection.append(self.record)
        records = self.collection.findall('record')
        assert len(records) > 0

    def test_append_leader(self):
        """Appending the leader works and has correct content"""
        found_leader = self.collection.find('./record/leader')
        assert found_leader.text == '     ntm a22      c 4500'

    def test_append_controlfield(self):
        """Appending a controlfield works correctly"""
        found_controlfield = self.collection.find('./record/controlfield')
        assert found_controlfield.text == 'tu' and \
               found_controlfield.get('tag') == '007'

    def test_append_datafield(self):
        """Appending a datafield works correctly"""
        found_datafield = self.collection.find('./record/datafield')
        found_subfields = found_datafield.findall('./subfield')
        assert not found_datafield.text and \
               found_datafield.get('tag') == '041' and \
               found_datafield.get('ind1') == ' ' and \
               found_datafield.get('ind2') == '1' and \
               found_subfields[0].get('code') == 'a' and \
               found_subfields[1].get('code') == 'c' and \
               found_subfields[0].text == 'ger' and \
               found_subfields[1].text == 'eng'
