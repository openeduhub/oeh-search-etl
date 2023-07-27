
import sys
import datetime as dt
import time
from typing import Callable, Optional

from scrapy.cmdline import execute as scrapy_execute

from schulcloud.util import Environment
from schulcloud.h5p.upload import Uploader as H5PUploader
from schulcloud.fwu.upload_fwu import Uploader as FWU_Uploader
from schulcloud.permission_updater import PermissionUpdater
from schulcloud.oeh_importer import OehImporter


needed_env_vars = [
    'CRAWLER',
    'SCHEDULE',  # semi colon seperated list of ScheduleRule strings
]


check_interval_seconds = 60


class ScheduleRule:
    """
    Rule which defines a schedule of the format 'month-day-hour:minute'

    Examples:
    ScheduleRule('1-31-3:30')  # Jan 1st 3:30 am
    ScheduleRule('*-Sa-1:00')  # every Saturday 1:00 am
    ScheduleRule('*-*-22:00')  # everyday 10:00 pm

    month   day                 hour:min
    1-12    1-31 or Mo-Su       0-23:0-59
    """

    weekdays = ['*', 'mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']

    @staticmethod
    def monthsdays(year: int, month: int):
        leap = ((not year % 4) if year % 100 else False) if year % 400 else True
        return 30 + ((month - 1) % 7 + 1) % 2 if not month == 2 else (28 if not leap else 29)

    @staticmethod
    def skip_month(date: dt.date):
        return dt.date(date.year+1 if date.month == 12 else date.year, date.month+1, 1)

    def __init__(self, string: str):
        try:
            month, day, tm = string.split('-')
            hour, min = tm.split(':')
            if not (day.isdigit() or day.lower() in self.weekdays):
                raise ValueError()
            self.month = int(month) if not month == '*' else 0
            if day.isdigit():
                self.dayofmonth = int(day)
                self.dayofweek = 0
            else:
                self.dayofmonth = 0
                self.dayofweek = self.weekdays.index(day.lower())
            self.time = dt.time(hour=int(hour), minute=int(min))
            if not (
                0 <= self.month <= 12 and
                0 <= self.dayofmonth <= 31 and
                not (self.dayofmonth and self.dayofweek)
            ):
                raise ValueError()
        except:
            raise ValueError(f'Invalid date time rule: {string}')

    def day_matches(self, date: dt.date):
        if (self.month and not date.month == self.month) or \
                (self.dayofmonth and not date.day == self.dayofmonth) or \
                (self.dayofweek and not date.weekday() + 1 == self.dayofweek):
            return False
        else:
            return True

    def next_datetime(self, now: Optional[dt.datetime] = None):
        if now is None:
            now = dt.datetime.now()

        if self.day_matches(now.date()):
            if now.time() < self.time:
                return dt.datetime.combine(now.date(), self.time)
            else:
                _next = now.date() + dt.timedelta(days=1)
        else:
            _next = now.date()

        while True:
            if self.month:
                if _next.month > self.month:
                    _next = dt.date(_next.year+1, self.month, 1)
                else:
                    _next = dt.date(_next.year, self.month, 1)
            if self.dayofmonth:
                if _next.day > self.dayofmonth:
                    _next = self.skip_month(_next)
                    continue
                _next = dt.date(_next.year, _next.month, min(self.dayofmonth, self.monthsdays(_next.year, _next.month)))
            elif self.dayofweek:
                if not _next.weekday() == self.dayofweek - 1:
                    days_in_future = (self.dayofweek - 1 - _next.weekday()) % 7
                    if _next.day + days_in_future > self.monthsdays(_next.year, _next.month):
                        _next = self.skip_month(_next)
                        continue
                    _next = dt.date(_next.year, _next.month, _next.day + days_in_future)
            break

        return dt.datetime.combine(_next, self.time)

    def __str__(self):
        return f'{str(self.month or "*")}-{str(self.dayofmonth)}'


class Job:
    def __init__(self, name: str, function: Callable, schedule: list[str]):
        self.name = name
        self.function = function
        self.schedule_rules = []
        if 'now' not in schedule:
            for rule in schedule:
                self.schedule_rules.append(ScheduleRule(rule))
            if not self.schedule_rules:
                raise ValueError('No schedule')

    def run_schedule(self):
        if not self.schedule_rules:
            self.run()
            return
        while True:
            now = dt.datetime.now()
            next_time = self.schedule_rules[0].next_datetime(now=now)
            for rule in self.schedule_rules[1:]:
                rules_next = rule.next_datetime(now=now)
                if rules_next < next_time:
                    next_time = rules_next

            print(f'Next run: {next_time} / in {str(next_time - now).split(".")[0]}', file=sys.stderr)

            while True:
                time_remaining = next_time - dt.datetime.now()
                if time_remaining.total_seconds() > 0.0:
                    time.sleep(min(time_remaining.total_seconds(), check_interval_seconds))
                    continue

                self.run()
                break

    def run(self):
        self.function()


def main():
    env = Environment(env_vars=needed_env_vars)
    schedule = env['SCHEDULE'].split(';')
    crawler = env['CRAWLER'].lower()
    if crawler == 'hello_world':
        job = Job('Hello World', lambda: print('Hello, world!', file=sys.stderr), schedule)
    elif crawler == 'h5p_upload':
        job = Job('H5P Uploader', H5PUploader().upload_from_s3, schedule)
    elif crawler == 'fwu_upload':
        # Time to upload FWU ~20min
        job = Job('FWU Uploader', FWU_Uploader().upload, schedule)
    elif crawler == 'permission_updater':
        job = Job('Permission Updater', PermissionUpdater().run, schedule)
    elif crawler == 'oeh_importer':
        job = Job('OEH Importer', OehImporter().run, schedule)
    elif crawler.endswith('spider'):
        job = Job(
            f'Crawler {crawler}',
            lambda: scrapy_execute(argv=['scrapy', 'crawl', crawler, '-s', 'TELNETCONSOLE_ENABLED=0']),
            schedule
        )
    else:
        print(f'Unexpected execution target "{crawler}"', file=sys.stderr)
        return 1

    job.run_schedule()
    return 0


if __name__ == '__main__':
    sys.exit(main())
