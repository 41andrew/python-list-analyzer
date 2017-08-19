# from model.input_row import Category


class EngagementStrategy:

    def __init__(self, input_row):
        self.input_row = input_row

    def assign_category(self):

        if self.input_row.has_any_engagements():
            print("Input has engagements")
            sample_engagement = self.input_row.engagements[0]

            if EngagementStrategy.is_input_row_in_capital_group(sample_engagement):
                # TODO harder case
                print("Engagement is in capital group - to be implemented")
            else:
                print("Engagement is not in capital group")

                for engagement in self.input_row.engagements:

                    if EngagementStrategy.is_input_row_restricted_by_description_or_status(engagement):
                        # TODO Category 3
                        print("Engagement is restricted - category 3")
                        break
                        # return Category.NOT_ACCEPTED

                # TODO pass toProposalStrategy
                print("Engagement is not restricted - go to proposal")
                # self.input_row.category = Category.ACCEPTED
                # self.input_row.category=   PrposalSrategry(self.input_row).ass
                # return Category.ACCEPTED

        else:
            # TODO pass to ProposalStrategy
            print("input has 0 engagements - go to proposal")
            # print("Entity {} capital group {}".format(self.input_row, Category.ACCEPTED))
            # return Category.ACCEPTED

    @staticmethod
    def is_input_row_in_capital_group(engagement):
        return engagement.entity.is_in_capital_group()

    @staticmethod
    def is_input_row_restricted_by_description_or_status(engagement):
        return engagement.entity.is_restricted() or engagement.is_active()






# nation_account - same in 3
# description - same in 2/3
# status - diff eng and prop
# entity_name - same in 2

