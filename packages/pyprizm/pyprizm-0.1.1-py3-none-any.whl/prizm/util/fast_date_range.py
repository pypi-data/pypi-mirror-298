from datetime import date, timedelta


class fastDateRange:
    @staticmethod
    def run(startDate: date, endDate: date, endInclusive=False):
        """
        A quicker way to create a range of dates using the datetime.date datatype than most others I have found. E.g. pandas
        seems o be slow and have a lot of overhead when there is a large volume.

        This will generate a date range including every date from StartDate to EndDate, with the endCapDate being explicitly
        included if endInclusive=True

        The default option of endInclusive=False is present to maintain consistency with

        :param startDate:
        :param endDate:
        :param endInclusive:
        :return:
        """
        for i in range((endDate - startDate).days + endInclusive * 1):
            yield startDate + timedelta(days=i)

    @staticmethod
    def runNDays(startDate: date, nDays: int):
        """
        alternate form of fastDateRange
        :param startDate:
        :param nDays:
        :return:
        """
        endDate = startDate + timedelta(days=nDays)
        return fastDateRange.run(
            startDate=startDate, endDate=endDate, endInclusive=False
        )

    @staticmethod
    def interval(startDate: date, endDate: date, interval: int):
        """
        alternate form of fastDateRange
        :param startDate:
        :param nDays:
        :return:
        """
        total_days = (endDate - startDate).days
        num_intervals = (
            total_days + interval
        ) // interval  # + interval_days to include end date if necessary

        # Generate the date range
        dates = [
            startDate + timedelta(days=interval * i) for i in range(num_intervals + 1)
        ]
        for d in dates:
            yield d
