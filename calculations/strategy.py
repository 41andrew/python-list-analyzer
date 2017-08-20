import abc
from model.input_row import Category


class InputRowsCategoryAssignmentContext:
    """
    Base class responsible for category assignment
    It takes strategy and produces result - all input rows will have category
    It does not depend from algorithm - may accept different implementations
    If in future algorithm will change - a different strategy will be passed
    """

    def __init__(self):
        self._strategy = None
        self._input_rows = None

    def run_category_assignment(self):
        for row in self._input_rows:
            print("ROW = {}".format(self._input_rows[row]))
            self._strategy.assign_category(self._input_rows[row])


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
    def end_of_calculation_if_row_not_in_capital_group(rows):

        if CategoryAssignmentStrategy.is_any_company_restricted(rows):
            # category is already assigned - no need to go deeper
            return True
        else:
            print("Category 1 and go deeper")
            return False

    def end_of_calculation_if_row_in_capital_group(self, rows, input_row):

        output_category = self.is_any_company_restricted_and_its_same_company_as_checked(rows, input_row)

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
    def is_any_company_restricted(rows):
        is_input_company_restricted = False

        for row in rows:
            if CategoryAssignmentStrategy.is_input_row_restricted_by_description_or_status(row):
                print("Row with NIP [{}] is restricted - category 3".format(row.entity.nip))
                is_input_company_restricted = True
                break

        return is_input_company_restricted

    @staticmethod
    def is_any_company_restricted_and_its_same_company_as_checked(rows, input_row):
        """
        Returns :
        1 - none of the rows is restricted
        2 - there was a restricted row BUT it was DIFFERENT company than input one
        3 - there was a restricted row AND it was THE SAME company as input
        """
        any_company_restricted = False
        restricted_company_is_same_as_input = False

        for row in rows:
            if CategoryAssignmentStrategy.is_input_row_restricted_by_description_or_status(row):
                any_company_restricted = True

                if input_row.is_entity_name_same_as_crm_name(row.entity.entity_name):
                    print("There is a restricted company and it's same as input one - category 3")
                    restricted_company_is_same_as_input = True

                    return 3

        if any_company_restricted and not restricted_company_is_same_as_input:
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

    def end_of_calculation_if_row_in_capital_group(self, rows, input_row):

        print("method end of in Proposal Strategy")
        output_category = self.is_any_company_restricted_and_its_same_company_as_checked(rows, input_row)

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