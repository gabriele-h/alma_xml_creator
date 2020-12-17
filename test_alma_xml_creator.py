"""
Tests for XML creation
"""

import pytest
from csv import reader, writer
from io import StringIO
from xml.etree import ElementTree

from alma_xml_creator import MarcCollection, create_collection_from_reader


class TestCreateCollectionFromReader:
    """
    With a dummy DictReader, is the xml created as expected?
    """

    csvfile = StringIO()
    csvfile.seek(0)
    csvwriter = writer(csvfile, delimiter=';')
    csvwriter.writerow(['leader', '007', '008', '041  ', '24500', '24610', '500  ', '500  '])
    csvwriter.writerow(
        [
            '     ntm a22      c 4500',
            'tu',
            '######|2020####|||###########|||#|#ger#c',
            '$$ager$$aeng',
            '$$aTest titles are best titles',
            '$$azehn',
            '$$aThematisches',
            '$$aSchlagwort'
        ]
    )
    csvwriter.writerow(
        [
            '     ntm a22      c 4500',
            'tu',
            '######|2020####|||###########|||#|#ger#c',
            '$$ager',
            '$$aBest titles are test titles',
            '$$azehn',
            '$$aThematisches',
            ''
        ]
    )
    csvfile.seek(0)
    csv_reader = reader(csvfile, delimiter=';')
    collection = create_collection_from_reader(csv_reader)

    def test_title_created_correctly(self):
        xpath_title = './record/datafield[@tag="245"]/subfield[@code="a"]'
        titles = self.collection.findall(xpath_title)
        assert titles[0].text == 'Test titles are best titles' and \
               titles[1].text == 'Best titles are test titles'

    def test_count_500(self):
        xpath_500 = './/datafield[@tag="500"]'
        all_500 = self.collection.findall(xpath_500)
        from xml.etree.ElementTree import tostring
        print(tostring(self.collection))
        assert len(all_500) == 3


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
    subfields = """$$ager$$ceng"""
    datafield = TestRecord.append_datafield('041 1', subfields)

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
