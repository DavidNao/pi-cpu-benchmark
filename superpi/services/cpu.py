# https://stackoverflow.com/questions/33406601/how-to-get-the-cpu-usage-of-past-10-minutes-in-python
def calculate(t1, t2):
    # from psutil.cpu_percent()
    # see: https://github.com/giampaolo/psutil/blob/master/psutil/__init__.py
    t1_all = sum(t1)
    t1_busy = t1_all - t1.idle
    t2_all = sum(t2)
    t2_busy = t2_all - t2.idle
    if t2_busy <= t1_busy:
        return 0.0
    busy_delta = t2_busy - t1_busy
    all_delta = t2_all - t1_all
    busy_perc = (busy_delta / all_delta) * 100
    return round(busy_perc, 1)
