import unittest
from unittest.mock import patch, MagicMock
from fast_check import Check


class TestCheck(Check):
    def __init__(self):
        super().__init__("http://example.org")

    def process(self, response):
        self.response = response


class TestFastCheck(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_check(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '{"id":1}'.encode("utf-8")
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        check = TestCheck()
        check.check()
        self.assertEqual(check.response, {"id": 1})


if __name__ == "__main__":
    unittest.main()