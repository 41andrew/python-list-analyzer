import unittest

from data_loader.data_loader import CsvDataLoader


class TestCsvDataLoader(unittest.TestCase):

    def setUp(self):
        self.data_loader = CsvDataLoader()

    def test_read_lines_from_file_file_not_exists(self):
        self.data_loader.data_paths["key_for_invalid_path"] = "not_existing_file.csv"
        self.assertRaises(FileNotFoundError, self.data_loader._read_lines_from_file("key_for_invalid_path"))

    def test_parse_object_from_semicolon_separated_line_wrong_formatting_bda(self):
        line = "1111111111;PZU S.A.;Alior Bank S.A.;audit restricted client - PL SLP assigned;11111;Spotkanie" \
               ";niewazne;16.02.2017;Jan Kowalski"

        self.assertRaises(IndexError,
                          self.data_loader._parse_object_from_semicolon_separated_line(line, "input_file_bda"))

    def test_parse_object_from_semicolon_separated_line_wrong_formatting_engagement(self):
        line = "4444444444;none;Spółka 1;audit restricted client - PL Secondary approval;Jan Kowalski;21-02-2015;Active"

        self.assertRaises(IndexError,
                          self.data_loader._parse_object_from_semicolon_separated_line(line, "input_file_engagements"))

    def test_parse_object_from_semicolon_separated_line_wrong_formatting_proposal(self):
        line = "1111111111;Grupa Test sp. zoo;Test sp. zoo;non-audit client / PL SLP;XXXXX3;bez znaczenia;Jan ;;;" \
               "Kowalski;19.02.2015;New"

        self.assertRaises(TypeError,
                          self.data_loader._parse_object_from_semicolon_separated_line(line, "input_file_proposals"))

if __name__ == "__main__":
    unittest.main()
