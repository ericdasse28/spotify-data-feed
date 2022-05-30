import datetime


class Context:
    def __init__(self):
        self.reference_day = "2022-05-21"
        self.reference_date = datetime.datetime.strptime(self.reference_day, "%Y-%m-%d")
        self.reference_date_str = datetime.datetime.strftime(
            self.reference_date, "%b %d, %Y"
        )


def make_test_dates():
    context = Context()
    test_dates = [(None, context.reference_day), (context.reference_day, None)]
    return test_dates
