# https://en.wikipedia.org/wiki/JJY

import time
from collections import OrderedDict

from radio_clock.jjy.segments import Year, Hours, Minutes, Day_of_Year, Day_of_Week


IDX_P3 = -4
M = P0 = P1 = P2 = P3 = P4 = P5 = 'M'
LS1 = LS2 = SU1 = SU2 = Reserved = 0

SYMBOLS_DUTY_CYCLE = {0: {1: 0.8, 0: 0.2}, 1: {1: 0.5, 0: 0.5}, 'M': {1: 0.2, 0: 0.8}}



def even_parity(bits):
    return 1 if sum(bits) % 2 else 0



class Encoder:

    @classmethod
    def get_time_code(cls, time_stamp = None):
        t = time.localtime(time_stamp or time.time())

        bits_hours = Hours.get_bits(t.tm_hour)
        PA1 = even_parity(bits_hours)

        bits_minutes = Minutes.get_bits(t.tm_min)
        PA2 = even_parity(bits_minutes)

        bits_year = Year.get_bits(t.tm_year)

        bits_day_of_year = Day_of_Year.get_bits(t.tm_yday)
        bits_day_of_year.insert(IDX_P3, P3)

        tm_wday = (t.tm_wday + 1) % 7  # Windows
        bits_day_of_week = Day_of_Week.get_bits(tm_wday)

        time_code = OrderedDict({'M'          : [M],
                                 'Minutes'    : bits_minutes,
                                 'P1'         : [P1],
                                 'Reserved_1' : [Reserved] * 2,
                                 'Hours'      : bits_hours,
                                 'P2'         : [P2],
                                 'Reserved_2' : [Reserved] * 2,
                                 'Day_of_Year': bits_day_of_year,
                                 'Reserved_3' : [Reserved] * 2,
                                 'PA1'        : [PA1],
                                 'PA2'        : [PA2],
                                 'SU1'        : [SU1],
                                 'P4'         : [P4],
                                 'SU2'        : [SU2],
                                 'Year'       : bits_year,
                                 'P5'         : [P5],
                                 'Day_of_Week': bits_day_of_week,
                                 'LS1'        : [LS1],
                                 'LS2'        : [LS2],
                                 'Reserved_4' : [Reserved] * 4,
                                 'P0'         : [P0]})

        return time_code


    @classmethod
    def get_bits(cls, time_stamp = None):
        bits = []
        time_code = cls.get_time_code(time_stamp)
        for v in time_code.values():
            bits += v
        return bits


    @classmethod
    def get_symbols(cls, time_stamp = None):
        return ''.join(['{}'.format(b) for b in cls.get_bits(time_stamp)])



class Decoder:

    @classmethod
    def get_time(cls, bits):
        yday_bits = bits[Day_of_Year.SECOND_RANGE_START: Day_of_Year.SECOND_RANGE_END][:]
        yday_bits.pop(IDX_P3 - 1)
        yday = Day_of_Year.get_value(yday_bits)

        yyyy = Year.get_value(bits[Year.SECOND_RANGE_START: Year.SECOND_RANGE_END])
        hh = Hours.get_value(bits[Hours.SECOND_RANGE_START: Hours.SECOND_RANGE_END])
        mm = Minutes.get_value(bits[Minutes.SECOND_RANGE_START: Minutes.SECOND_RANGE_END])

        ts = time.strptime('{}-{} {}:{}'.format(yyyy, yday, hh, mm), '%Y-%j %H:%M')
        # MicroPython: (year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
        return time.mktime(ts)
