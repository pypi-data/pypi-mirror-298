from ffquant.indicators.BaseIndicator import BaseIndicator
from datetime import datetime, timedelta
import pytz

__ALL__ = ['TurningPoint']

class TurningPoint(BaseIndicator):
    (TURNING_DN, NA, TURNING_UP) = (-1, 0, 1)

    lines = ('tp',)

    def __init__(self):
        self.addminperiod(1)
        self.cache = {}

    def handle_api_resp(self, item):
        result_time_str = datetime.fromtimestamp(item['openTime']/ 1000).strftime('%Y-%m-%d %H:%M:%S')
        if item.get('TYPE_TURNING_POINT', None) is not None and item['TYPE_TURNING_POINT'] == 'TURNING_UP':
            self.cache[result_time_str] = self.TURNING_UP
        elif item.get('TYPE_TURNING_POINT', None) is not None and item['TYPE_TURNING_POINT'] == 'TURNING_DN':
            self.cache[result_time_str] = self.TURNING_DN

        if self.p.debug:
            print(f"{self.__class__.__name__}, result_time_str: {result_time_str}, type_turning_point: {item['TYPE_TURNING_POINT'] if item.get('TYPE_TURNING_POINT', None) is not None else None}") 


    def backpeek_for_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        self.lines.tp[0] = self.cache.get(current_bar_time_str, self.NA)
        for i in range(0, self.p.backpeek_size):
            v = self.cache.get((current_bar_time - timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S'), self.NA)
            if v != self.NA:
                if self.p.debug:
                    print(f"{self.__class__.__name__}, backpeek_size: {i}, v: {v}")
                self.lines.tp[0] = v
                break