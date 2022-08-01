import datetime
import time


class getTime:
    def __init__(self):
        self.year = datetime.datetime.today().year
        self.month = datetime.datetime.today().month
        self.day = datetime.datetime.today().day
        self.time = time.strftime("%H:%M:%S", time.localtime())

    def returnAllTime(self):
        return "%s/%s/%s %s" % (self.year, self.month, self.day, self.time)

    def returnStrDate(self):
        return "%s-%s-%s" % (self.year, self.month, self.day)

    def returnYear(self):
        return "%s" % self.year

    def returnMouth(self):
        return "%s" % self.month

    def returnDay(self):
        return "%s" % self.day

    def timeRange(self, dateStart, dateEnd, endTime):
        start_time = datetime.datetime.strptime(dateStart + endTime, '%Y-%m-%d%H:%M:%S')
        end_time = datetime.datetime.strptime(dateEnd + endTime, '%Y-%m-%d%H:%M:%S')
        now_time = datetime.datetime.now()
        if start_time < now_time < end_time:
            return True
        else:
            return False
