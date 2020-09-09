import unittest

from calculations.strategy import *
from model.engagement import Engagement
from model.entity import Entity


class CategoryAssignmentStrategyTest(unittest.TestCase):

    def setUp(self):
        self.__context = InputRowsCategoryAssignmentContext()
        self.__strategy = EngagementStrategy()
        self.__input_rows = {}

        self.__context._strategy = self.__strategy

    def test_is_input_row_in_capital_group_should_be_true(self):
        entity = Entity("1111111111", "Grupa Test sp. zoo",
                                "Test sp. zoo", "audit restricted client - PL SLP assigned")
        engagement = Engagement(entity, "XXXXX1", "bez znaczenia", "Jan Kowalski", "21-02-2015", "Active")

        self.assertTrue(self.__strategy.is_input_row_in_capital_group(engagement), msg="Should be in capital group")

    def test_is_input_row_in_capital_group_should_be_false1(self):
        entity = Entity("1111111111", "Other",
                                "Test sp. zoo", "audit restricted client - PL SLP assigned")
        engagement = Engagement(entity, "XXXXX1", "bez znaczenia", "Jan Kowalski", "21-02-2015", "Active")

        self.assertFalse(self.__strategy.is_input_row_in_capital_group(engagement), msg="Should not be in capital group")

    def test_is_input_row_in_capital_group_should_be_false2(self):
        entity = Entity("1111111111", "",
                                "Test sp. zoo", "audit restricted client - PL SLP assigned")
        engagement = Engagement(entity, "XXXXX1", "bez znaczenia", "Jan Kowalski", "21-02-2015", "Active")

        self.assertFalse(self.__strategy.is_input_row_in_capital_group(engagement), msg="Should not be in capital group")

    def test_is_input_row_in_capital_group_should_be_false3(self):
        entity = Entity("1111111111", "None",
                                "Test sp. zoo", "audit restricted client - PL SLP assigned")
        engagement = Engagement(entity, "XXXXX1", "bez znaczenia", "Jan Kowalski", "21-02-2015", "Active")

        self.assertFalse(self.__strategy.is_input_row_in_capital_group(engagement), msg="Should not be in capital group")

    def test_is_input_row_in_capital_group_should_be_false4(self):
        entity = Entity("1111111111", "other",
                                "Test sp. zoo", "audit restricted client - PL SLP assigned")
        engagement = Engagement(entity, "XXXXX1", "bez znaczenia", "Jan Kowalski", "21-02-2015", "Active")

        self.assertFalse(self.__strategy.is_input_row_in_capital_group(engagement), msg="Should not be in capital group")

if __name__ == "__main__":
    unittest.main()
