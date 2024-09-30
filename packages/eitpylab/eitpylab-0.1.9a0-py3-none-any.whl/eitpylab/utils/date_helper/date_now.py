from datetime import datetime


class DateNow:
    """
    Utility class for obtaining the current date and time in a specific format.

    Methods:
        getNow() -> str:
            Get the current date and time.

            Returns:
                str: Current date and time in the format "yyyy-mmMMM-dd_hh-mm-ss" (hours in 24h format).
    """

    @staticmethod
    def getNow():
        """
        Get current date and time in the following format: 2020-08Aug-31_13-19-04 hours in 24h format

        Returns:
            str: Current date and time.
        """
        return datetime.now().strftime("%Y-%m%b-%d_%H-%M-%S")
