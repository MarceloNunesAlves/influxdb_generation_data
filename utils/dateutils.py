from datetime import datetime
from datetime import timedelta
import pandas as pd

class dateutils():
    def __init__(self):
        pass

    def days_between(self, d1, d2):
        return abs((d2 - d1).days) > 0

    def numDaysBetween(self, d1, d2):
        return abs((d2 - d1).days)

    def numMinutesBetween(self, d1, d2):
        return abs((d2 - d1).minutes)

    def dataAtual(self):
        return datetime.utcnow() #Usar UTC

    def convertDateToStr(self, d):
        return datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')

    def convertDateToStr2(self, d):
        return datetime.strptime(d, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    def convertStrToDate(self, d):
        return datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')

    def convertStrToDateFull(self, d):
        return datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.000Z')

    def rangeDates(self, dt ,numDays):
        return [x.strftime("%Y-%m-%d") for x in pd.date_range(dt, periods=numDays).to_pydatetime().tolist()]

    def rangeMinutes(self, dt_ini ,dt_fin):
        return [x for x in pd.date_range(dt_ini, dt_fin, freq="1min").to_pydatetime().tolist()]

    def addDays(self, dt, numDays):
        return (datetime.strptime(dt, '%Y-%m-%d') + timedelta(days=numDays)).strftime("%Y-%m-%d")

    def addDaysDateFull(self, dt, numDays):
        return (datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(days=numDays)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def addMinutesDateStr(self, dt, numMinutes):
        return (datetime.strptime(dt+'T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(minutes=numMinutes)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def addMinutes(self, dt, numMinutes):
        return (dt + timedelta(minutes=numMinutes))

    def addMinutesDate(self, dt, numMinutes):
        return (dt + timedelta(minutes=numMinutes)).strftime("%Y-%m-%dT%H:%M:%S.000Z")