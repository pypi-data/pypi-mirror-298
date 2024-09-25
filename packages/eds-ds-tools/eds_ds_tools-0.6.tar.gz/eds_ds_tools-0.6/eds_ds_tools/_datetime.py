__all__ = ['DtFind']

from ._imports import *

class DtFind:

    @staticmethod
    def previous_day(dt_, dt_format=None):
        d = dt_ - dt.timedelta(1)
        if dt_format:
            d = d.strftime(dt_format)
        return d

    @staticmethod
    def first_day_of_month(dt_, dt_format=None):
        d = dt_.replace(day=1)
        if dt_format:
            d = d.strftime(dt_format)
        return d
    
    @classmethod
    def first_day_last_month(cls, dt_, dt_format=None):
        d = cls.first_day_of_month(cls.first_day_of_month(dt_) - dt.timedelta(days=1))
        if dt_format:
            d = d.strftime(dt_format)
        return d
    
    @classmethod
    def first_day_next_month(cls, dt_, dt_format=None):
        d = cls.first_day_of_month(dt_.replace(day=28) + dt.timedelta(days=4))
        if dt_format:
            d = d.strftime(dt_format)
        return d
    
    @classmethod
    def last_day_of_month(cls, dt_, dt_format=None):
        d = cls.first_day_next_month(dt_) - dt.timedelta(days=1)
        if dt_format:
            d = d.strftime(dt_format)
        return d
