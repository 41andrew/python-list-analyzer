import abc


class BaseRow(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def print_attributes_separated_by_semicolon(self):
        """
            Method returns object attributes (only simple ones - no collections or other objects) as string
            separated by semicolon\n
            f.ex 'property1;property2;property3'
        """
        pass
