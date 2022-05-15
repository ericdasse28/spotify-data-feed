import datetime


class Context:
    def __init__(self):
        self.reference_day = "2022-05-03"
        self.reference_date = datetime.datetime.strptime(self.reference_day, "%Y-%m-%d")
        self.reference_date_str = datetime.datetime.strftime(
            self.reference_date, "%b %d, %Y"
        )
