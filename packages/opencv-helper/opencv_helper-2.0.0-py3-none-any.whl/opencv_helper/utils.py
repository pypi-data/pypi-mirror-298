import time


class Utils:
    def run_time(func):
        def inner(*args, **kwargs):
            t_start = time.time()
            res = func(*args, **kwargs)
            t_end = time.time()
            print(f"一共花费了{t_end - t_start}秒时间,函数运行结果是 {res}")
            return res

        return inner
