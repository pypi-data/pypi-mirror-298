# tests/test_parser.py
import unittest
from compiler.parser import JTMLParser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = JTMLParser()

    def test_parse_valid_jtml(self):
        root = self.parser.parse_jtml_file('tests/data/valid_component.jtml')
        self.assertIsNotNone(root)
        self.assertEqual(root.tag, 'component')

    def test_parse_invalid_jtml(self):
        with self.assertRaises(SystemExit):
            root = self.parser.parse_jtml_file('tests/data/invalid_component.jtml')
            self.parser.validate_component(root, 'tests/data/invalid_component.jtml')

    def test_parse_syntax_error_jtml(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_jtml_file('tests/data/invalid_component_syntax_error.jtml')


if __name__ == '__main__':
    unittest.main()
