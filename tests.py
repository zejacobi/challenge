import __builtin__
from unittest import TestCase
from json import dumps
from mock import patch, mock_open
import linkage


class TestImport(TestCase):
    @classmethod
    def setUpClass(cls):
        test_json = [{u'name': u'a'}, {u'name': u'b'}, {u'name': u'c'}, {u'name': u'd'}]
        cls.io = '\n'.join([dumps(line) for line in test_json])
        cls.json = test_json
        cls.sets = ([test_json[3], test_json[1], test_json[2]], [test_json[0]])

    def test_import_json_file(self):
        with patch.object(__builtin__, 'open', mock_open(read_data=self.io)):
            self.assertEqual(linkage.import_json_file('test.txt'), self.json)

    def test_cross_validation_sets(self):
        self.assertEqual(linkage.cross_validation_sets(self.json, 0.75), self.sets)


class TestParsingAndAnalysis(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product_json = [{u'product_name': u'Canon_PowerShot_S20', u'manufacturer': u'Canon',
                            u'model': u'S20', u'family': u'PowerShot',
                            u'announced-date': u'2000-01-05T19:00:00.000-05:00'}]
        cls.listing_json = [{u'title': u'Canon PowerShot S20 3.2MP Digital Camera w/ 2x Optical Zoom',
                            u'manufacturer': u'Canon USA', u'currency': u'USD', u'price': 59.50}]
        cls.product_tags = [{u'name_tags': [u'PowerShot', u'Canon', u'S20'], u'manufacturer_tags': [u'Canon']}]
        cls.listing_tags = [{u'name_tags': [u'Optical', u'w/', u'2x', u'PowerShot', u'Canon', u'3.2MP', u'Zoom', u'S20',
                                            u'Camera', u'Digital'],
                             u'manufacturer_tags': [u'Canon', u'USA']}]
        cls.matches = {0: [0]}
        
    def test_parse_products(self):
        self.assertEqual(linkage.parse_products(self.product_json), self.product_tags)

    def test_parse_listings(self):
        self.assertEqual(linkage.parse_listings(self.listing_json), self.listing_tags)

    def test_matching_product_words(self):
        self.assertEqual(linkage.matching_product_words(self.product_tags, self.listing_tags, 2), self.matches)