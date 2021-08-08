from typing import List

from datetime import date
from dateutil import relativedelta


def generateMonthlyDateRange(startDate: date, endDate: date) -> List[date]:
    date_modified = startDate
    dateList = [startDate]

    while date_modified < endDate:
        date_modified += relativedelta.relativedelta(months=1)
        dateList.append(date_modified)

    return dateList
