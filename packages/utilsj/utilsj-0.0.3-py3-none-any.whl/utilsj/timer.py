#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by zj on 2020/10/13 
# Task:
from collections import deque
from datetime import datetime
import time
import cv2

__all__ = ['FPSRealTime', 'FPS', 'MyTimer', 'runtime']


class FPSRealTime(object):
    def __init__(self, buffer_len=10):
        self._start_tick = cv2.getTickCount()
        self._freq = 1000.0 / cv2.getTickFrequency()
        self._difftimes = deque(maxlen=buffer_len)

    def get_fps(self, number=2):
        current_tick = cv2.getTickCount()
        different_time = (current_tick - self._start_tick) * self._freq
        self._start_tick = current_tick

        self._difftimes.append(different_time)

        fps = 1000.0 / (sum(self._difftimes) / len(self._difftimes))
        fps_rounded = round(fps, number)

        return fps_rounded


class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def get_fps(self):
        # compute the (approximate) frames per second
        return round(self._numFrames / self.elapsed(), 2)


class MyTimer2(object):
    def __init__(self):
        self.first_start_time = self.restart()

    def restart(self):
        self.start_time = time.time()
        return self.start_time

    def elapsed(self, restart=False, unit='ms'):
        assert unit in ('us', 'ms', 's', 'min')
        duration = (time.time() - self.start_time)
        if unit == 'us':
            duration = duration * 1e6
        elif unit == 'ms':
            duration = duration * 1e3
        elif unit == 's':
            duration = duration
        elif unit == 'min':
            duration = duration / 60
        if restart:
            self.restart()
        return duration

    def log(self, tip='Elapsed time', unit='ms', reset=False):
        duration = round(self.elapsed(reset, unit), 3)
        print('{}: {}{}'.format(tip, duration, unit))
        return duration

    def rlog(self, tip='Elapsed time'):
        return self.log(unit='ms', reset=True, tip=tip)

    def total_elapsed(self, unit='ms'):
        assert unit in ('us', 'ms', 's', 'min')
        duration = (time.time() - self.first_start_time)
        if unit == 'us':
            duration = duration * 1e6
        elif unit == 'ms':
            duration = duration * 1e3
        elif unit == 's':
            duration = duration
        elif unit == 'min':
            duration = duration / 60
        return duration


class MyTimer(object):
    def __init__(self, logger=None, debug=True):
        self._tickfrequency = cv2.getTickFrequency()
        self.first_start_time = self.restart()
        
        self.name2start_time = dict()
        self.logger = logger
        self.debug = debug


    def restart(self, name=""):
        tick_count = cv2.getTickCount()
        if name:
            self.name2start_time[name] = tick_count
        else:
            self._start_tick = tick_count
        return tick_count

    def elapsed(self, restart=False, unit='ms', name=""):
        if name and name not in self.name2start_time:
            msg = f'add point before using name: {name}'
            if self.logger:
                self.logger.warning(msg)
            else:
                print(msg)
            return 0
        assert unit in ('us', 'ms', 's', 'min')
        if name:
            start_tick = self.name2start_time[name]
        else:
            start_tick = self._start_tick
        duration = (cv2.getTickCount() - start_tick) / self._tickfrequency
        if unit == 'us':
            duration = duration * 1e6
        elif unit == 'ms':
            duration = duration * 1e3
        elif unit == 's':
            duration = duration
        elif unit == 'min':
            duration = duration / 60
        if restart:
            self.restart(name)
        return duration

    def log(self, tip='Elapsed time', unit='ms', reset=False, name=""):
        duration = round(self.elapsed(reset, unit, name=name), 3)
        msg = f'{tip}: {duration:.3f}{unit}'
        if self.logger:
            self.logger.debug(msg) if self.debug else self.logger.info(msg)
        else:
            print(msg)
        return duration

    def rlog(self, tip='Elapsed time', unit='ms', reset=True, name=""):
        return self.log(tip=tip, unit=unit, reset=reset, name=name)

    def total_elapsed(self, unit='ms'):
        assert unit in ('us', 'ms', 's', 'min')

        duration = (cv2.getTickCount() - self.first_start_time) / self._tickfrequency
        if unit == 'us':
            duration = duration * 1e6
        elif unit == 'ms':
            duration = duration * 1e3
        elif unit == 's':
            duration = duration
        elif unit == 'min':
            duration = duration / 60
        return duration

    def add_point(self, name='time1'):
        self.name2start_time[name] = cv2.getTickCount()


MYTIMER_ = MyTimer()


def runtime(func):
    def wrapper(*args, **kw):
        MYTIMER_.restart()
        ret = func(*args, **kw)
        MYTIMER_.rlog(f'func "{func.__name__}" run time')
        return ret

    return wrapper


def main():
    timer = MyTimer()
    sum = 0
    for i in range(int(10e6)):
        sum += i

    # timer.log(unit='us', reset=False)
    timer.log(unit='ms', reset=False)
    timer.log(unit='s', reset=False)
    # timer.log(unit='min', reset=False)


if __name__ == '__main__':
    start = datetime.now()
    print("Start time is {}".format(start))
    main()
    end = datetime.now()
    print("End time is {}".format(end))
    print("\nTotal running time is {}s".format((end - start).seconds))
    print("\nCongratulations!!!")
