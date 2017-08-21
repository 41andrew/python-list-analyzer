import abc
import timeit
from ..model.input_row import Category
from ..reporter.reporter import HtmlReporter


class InputRowsCategoryAssignmentContext:
    """
    Base class responsible for category assignment
    It takes strategy and produces result - all input rows will have category
    It does not depend from algorithm - may accept different implementations
    If in future algorithm will change - a different strategy will be passed
    """

    def __init__(self):
        self.__strategy = None
        self.input_rows = None
        self.reporter = HtmlReporter()

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, strategy):
        self.__strategy = strategy
        self.__strategy.__reporter = self.reporter

    def run_category_assignment(self):
        start_time = timeit.default_timer()

        for row in self.input_rows:
            print("ROW = {}".format(self.input_rows[row]))

            current_row = self.input_rows[row]
            self.strategy.assign_category(current_row)

        end_time = timeit.default_timer()

        self.reporter.set_execution_time((end_time - start_time))
        self.reporter.set_report_result(self.input_rows.values())


class CategoryAssignmentStrategy(metaclass=abc.ABCMeta):
    """
    Abstract strategy class
    """

    @abc.abstractmethod
    def assign_category(self, input_row):
        pass

    @staticmethod
    def is_input_row_in_capital_group(model):
        return model.entity.is_in_capital_group()

    @staticmethod
    def is_input_row_restricted_by_description_or_status(model):
        return model.entity.is_restricted() or model.is_active()

    @staticmethod
    def end_of_calculation_if_row_not_in_capital_group(collection):
        """
        Check if category is finally assign, when company from input row is NOT IN capital group.

        :param collection: list of objects - engagements/proposals etc
        :return: True if category is finally assigned. False if there is a need to pass input_row to another strategy
        """

        if CategoryAssignmentStrategy.is_any_company_restricted(collection):
            # category is already assigned - no need to go deeper
            return True
        else:
            print("Category 1 and go deeper")
            return False

    def end_of_calculation_if_row_in_capital_group(self, collection, input_row):
        """
        Check if category is finally assign, when company from input row is IN capital group.
        Category is assign inside this method

        :param collection: list of objects - engagements/proposals etc
        :param input_row: current row for which we want to assign category
        :return: True if category is finally assigned. False if there is a need to pass input_row to another strategy
        """

        output_category = self.is_any_company_restricted_and_its_same_company_as_checked(collection, input_row)

        if output_category == 3:
            input_row.category = Category.NOT_ACCEPTED
            return True
        elif output_category == 2:
            input_row.category = Category.TO_CHECK
            return False
        elif output_category == 1:
            input_row.category = Category.ACCEPTED
            return False

    @staticmethod
    def is_any_company_restricted(collection):
        """

        :param collection: list of objects - engagements/proposals etc
        :return:
        """

        is_input_company_restricted = False

        for model_object in collection:
            if CategoryAssignmentStrategy.is_input_row_restricted_by_description_or_status(model_object):
                print("Row with NIP [{}] is restricted - category 3".format(model_object.entity.nip))
                is_input_company_restricted = True
                break

        return is_input_company_restricted

    @staticmethod
    def is_any_company_restricted_and_its_same_company_as_checked(collection, input_row):
        """


        :param collection: collection: list of objects - engagements/proposals etc
        :param input_row: input_row: current row for which we want to assign category
        :return: 1 - none of the rows is restricted\n
                 2 - there was a restricted row BUT it was DIFFERENT company than input one\n
                 3 - there was a restricted row AND it was THE SAME company as input
        """

        any_company_restricted = False

        for model_object in collection:
            if CategoryAssignmentStrategy.is_input_row_restricted_by_description_or_status(model_object):
                any_company_restricted = True

                if input_row.is_entity_name_same_as_crm_name(model_object.entity.entity_name):
                    print("There is a restricted company and it's same as input one - category 3")
                    return 3

        if any_company_restricted:
            print("There was restricted company but different than input one - category 2, check further")
            return 2
        elif not any_company_restricted:
            print("There wasn't any restricted company - category 1, check further")
            return 1


class EngagementStrategy(CategoryAssignmentStrategy):

    def assign_category(self, input_row):

        if input_row.has_any_engagements():
            print("input_row with NIP [{}] has engagements - further check".format(input_row.nip))

            # Each row in engagements file for same NIP has some value of national_account
            sample_engagement = input_row.engagements[0]

            if self.is_input_row_in_capital_group(sample_engagement):
                print("Engagement is in capital group")

                if self.end_of_calculation_if_row_in_capital_group(input_row.engagements, input_row):
                    print("Category finally assigned in EngagementStrategy")
                else:
                    ProposalStrategy().assign_category(input_row)

            else:
                print("Engagement is not in capital group")

                if self.end_of_calculation_if_row_not_in_capital_group(input_row.engagements):
                    print("Category finally assigned in EngagementStrategy")
                    input_row.category = Category.NOT_ACCEPTED
                else:
                    input_row.category = Category.ACCEPTED
                    ProposalStrategy().assign_category(input_row)

        else:
            print("input_row with NIP [{}] has no engagements".format(input_row.nip))
            ProposalStrategy().assign_category(input_row)


class ProposalStrategy(CategoryAssignmentStrategy):

    def end_of_calculation_if_row_in_capital_group(self, collection, input_row):

        print("method end of in Proposal Strategy")
        output_category = self.is_any_company_restricted_and_its_same_company_as_checked(collection, input_row)

        if output_category == 3:
            input_row.category = Category.NOT_ACCEPTED
            return True
        elif output_category == 2:
            input_row.category = Category.TO_CHECK
            return True
        elif output_category == 1:
            input_row.category = Category.ACCEPTED
            return False

    def assign_category(self, input_row):

        if input_row.has_any_proposals():
            print("input_row with NIP [{}] has proposals - further check".format(input_row.nip))

            # Each row in engagements file for same NIP has some value of national_account
            sample_proposal = input_row.proposals[0]

            if self.is_input_row_in_capital_group(sample_proposal):
                print("Proposal is in capital group")

                if self.end_of_calculation_if_row_in_capital_group(input_row.proposals, input_row):
                    print("Category finally assigned in ProposalStrategy")
                else:
                    BDAStrategy().assign_category(input_row)

            else:
                print("Proposal is not in capital group")

                if self.end_of_calculation_if_row_not_in_capital_group(input_row.proposals):
                    print("Category finally assigned in ProposalStrategy")
                    input_row.category = Category.NOT_ACCEPTED
                else:
                    input_row.category = Category.ACCEPTED
                    BDAStrategy().assign_category(input_row)

        else:
            print("input_row with NIP [{}] has no proposals".format(input_row.nip))
            BDAStrategy().assign_category(input_row)


class BDAStrategy(CategoryAssignmentStrategy):

    def assign_category(self, input_row):
        print("Checking BDAs")

        if input_row.has_any_bdas():
            print("input_row with NIP [{}] has BDAa".format(input_row.nip))
            input_row.category = Category.TO_CHECK
