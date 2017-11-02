# Interface
class DataProcessor:
    """
    Data processors take data, process it, and outputs the results in some
    format. The way data is processed and output is dependent on the actual
    implementation.
    """

    def process(self, data):
        """
        Processes the given data and outputs the results.

        :param data: data loaded using a data loader
        """
