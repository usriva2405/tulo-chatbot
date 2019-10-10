import random
import re

# a regular expression for validating an Email
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


class UtilityFunctions:

    @staticmethod
    def is_email_valid(email):
        if re.search(regex, email):
            return True
        else:
            return False

    @staticmethod
    def get_random_number(upper_range):
        """
        get random number between 0 and upper range
        :return:
        """
        return int(random.randint(0, upper_range))
