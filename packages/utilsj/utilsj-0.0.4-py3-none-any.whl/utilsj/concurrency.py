#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by zj on 2022/04/20
# Task:

import concurrent.futures
import math
import threading
from datetime import datetime
from multiprocessing import Process

from tqdm import tqdm


def multi_task(target_func, args_lst, workers=1, verbose=True, thread_or_process='thread', return_result=True):
    """

    :param target_func: 目标函数
    :param args_lst: args_lst中每个元素是目标函数的参数。
    :param workers: 并发数
    :param verbose: 是否打印过程
    :param thread_or_process: 线程或进程
    :param return_result: 是否返回结果
    :return:
    """

    ret = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers) if thread_or_process == 'thread' else concurrent.futures.ProcessPoolExecutor(
            max_workers=workers) as executor:
        future_to_index = {executor.submit(
            target_func, *args): i for i, args in enumerate(args_lst)}
        with tqdm(total=len(args_lst), disable=verbose is False) as pbar:
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                if return_result:
                    ret.append((future.result(), index))
                pbar.update(1)
    if return_result:
        ret = sorted(ret, key=lambda x: x[1])
        ret = [x[0] for x in ret]
    else:
        ret = None
    return ret


class MyThread(threading.Thread):
    """
    通过obj.get_result()获取线程的输出
    """

    def __init__(self, target, args=()):
        super(MyThread, self).__init__()
        self.func = target
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


# TODO 多进程获取进程结果失败
class MyProcess(Process):
    """
    通过obj.get_result()获取进程的输出
    """

    def __init__(self, target, args=()):
        super(MyProcess, self).__init__()
        self.func = target
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def split_list(l, n):
    """
    把一个list n等分，最后一部分可以不是等分的。
    :param l: list.
    :param n: n等分.
    :return: list，每个元素又是一个list.
    """
    assert isinstance(l, list) and isinstance(n, int)
    if len(l) < n:
        n = len(l)
    split_lst = []
    step = int(math.ceil(len(l) / n))
    for i in range(0, len(l), step):
        split_lst.append(l[i:i + step])
    return split_lst


def multi_thread_task(target_func, args_lst, workers):
    """
    将待执行任务n等分，交由n个线程去执行。
    :param target_func: task
    :param args_lst: args_lst中每个元素也是list,且子list中的元素相等。
    :param workers: n
    :return:
    """
    args_split_lst = []
    for l in args_lst:
        if isinstance(l, list):
            arg = split_list(l, workers)
        else:
            arg = l
        args_split_lst.append(arg)
    thread_lst = []
    for i in range(len(args_split_lst[0])):
        args = []
        for arg in args_split_lst:
            if isinstance(arg, list):
                args.append(arg[i])
            else:
                args.append(arg)
        t = MyThread(target=target_func, args=tuple(args))
        thread_lst.append(t)
        t.start()
    for t in thread_lst:
        t.join()
    return thread_lst


def multi_process_task(target_func, args_lst, workers):
    """

    :param target_func:
    :param args_lst: args_lst中每个元素也是list,且子list中的元素相等。
    :param workers:
    :return:
    """
    args_split_lst = []
    for l in args_lst:
        if isinstance(l, list):
            arg = split_list(l, workers)
        else:
            arg = l
        args_split_lst.append(arg)
    process_lst = []
    for i in range(len(args_split_lst[0])):
        args = []
        for arg in args_split_lst:
            if isinstance(arg, list):
                args.append(arg[i])
            else:
                args.append(arg)
        t = MyProcess(target=target_func, args=tuple(args))
        process_lst.append(t)
        t.start()
    for t in process_lst:
        t.join()
    return process_lst


def main():
    pass


if __name__ == '__main__':
    start = datetime.now()
    print("Start time is {}".format(start))
    main()
    end = datetime.now()
    print("End time is {}".format(end))
    print("\nTotal running time is {}s".format((end - start).seconds))
    print("\nCongratulations!!!")
