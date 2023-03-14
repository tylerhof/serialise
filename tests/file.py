import unittest
from io import StringIO

from serialise.file import SaveDictsAsCsv
from tests.test_utils import FunctorTest


class FileTest(unittest.TestCase):
    def test_filter(self):
        FunctorTest.test(self, lambda x: SaveDictsAsCsv(StringIO())(x).value.getvalue(),
                         [{'a' : 1, 'b' : 2},{'a' : 'c', 'b' : 'd'}],
                         'a,b\r\n1,2\r\nc,d\r\n')

if __name__ == '__main__':
    unittest.main()