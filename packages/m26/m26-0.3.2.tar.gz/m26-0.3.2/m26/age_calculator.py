__author__ = "cjoakim"

from datetime import datetime
import traceback

from .age import Age


class AgeCalculator(object):

    @classmethod
    def seconds_per_year(cls):
        # seconds * minutes * hours * days
        return float(60 * 60 * 24 * 365.25)

    @classmethod
    def milliseconds_per_year(cls):
        return float(cls.seconds_per_year() * 1000.0)

    @classmethod
    def calculate(cls, birth_yyyy_mm_dd, as_of_yyyy_mm_dd):
        if birth_yyyy_mm_dd and as_of_yyyy_mm_dd:
            try:
                date_format = "%Y-%m-%d"
                birth_datetime = datetime.strptime(birth_yyyy_mm_dd, date_format)
                as_of_datetime = datetime.strptime(as_of_yyyy_mm_dd, date_format)
                delta = as_of_datetime - birth_datetime
                years = delta.total_seconds() / cls.seconds_per_year()
                return Age(float(years))
            except Exception as e:
                print("AgeCalculator#calculate() exception: {}".format(e))
                print(traceback.format_exc())
                return None
        else:
            return None
