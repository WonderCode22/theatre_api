from datetime import datetime, date, time
from dateutil import parser


class Utils:

    @staticmethod
    def end_of_date(dt):
        if type(dt) is datetime:
            return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif type(dt) is date:
            return datetime.combine(dt, time.max)

    @staticmethod
    def start_of_date(dt):
        if type(dt) is datetime:
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif type(dt) is date:
            return datetime.combine(dt, time.min)

    @staticmethod
    def safe_int(val, default=0):
        try:
            return int(val)
        except:
            return default

    @staticmethod
    def string_to_date(date_str, default=''):
        try:
            return parser.parse(date_str)
        except:
            return default

    @staticmethod
    def string_to_hour_minute(hour_minute_str):
        """
        Parse hour:time
        :param hour_minute_str: string : 10:30
        :return: 10, 30
        """
        try:
            data = hour_minute_str.split(':')
            return Utils.safe_int(data[0]), Utils.safe_int(data[1])
        except:
            return None, None