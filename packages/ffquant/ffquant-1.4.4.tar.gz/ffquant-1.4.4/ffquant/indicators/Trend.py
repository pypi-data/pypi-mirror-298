from ffquant.indicators.BaseIndicator import BaseIndicator
from datetime import datetime, timedelta
import pytz

__ALL__ = ['Trend']

class Trend(BaseIndicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    lines = ('trend',)

    def __init__(self):
        self.addminperiod(1)
        self.cache = {}

    def handle_api_resp(self, item):
        result_time_str = datetime.fromtimestamp(item['openTime']/ 1000).strftime('%Y-%m-%d %H:%M:%S')
        if item.get('TYPE_TREND', None) is not None and item['TYPE_TREND'] == 'BULLISH':
            self.cache[result_time_str] = self.BULLISH
        elif item.get('TYPE_TREND', None) is not None and item['TYPE_TREND'] == 'BEARISH':
            self.cache[result_time_str] = self.BEARISH

        if self.p.debug:
            print(f"{self.__class__.__name__}, result_time_str: {result_time_str}, type_trend: {item['TYPE_TREND'] if item.get('TYPE_TREND', None) is not None else None}")

    def backpeek_for_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        self.lines.trend[0] = self.cache.get(current_bar_time_str, self.NA)
        for i in range(0, self.p.backpeek_size):
            v = self.cache.get((current_bar_time - timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S'), self.NA)
            if v != self.NA:
                if self.p.debug:
                    print(f"{self.__class__.__name__}, backpeek_size: {i}, v: {v}")
                self.lines.trend[0] = v
                break