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