import time
from datetime import timedelta
import logging
from typing import List
import plotext as plx
import psutil
from multiprocessing import cpu_count
from .services.cpu import calculate
from .services.services import pi_monte_carlo_parallel

DEFAULT_NB_MILLION_POINTS = 100

logger = logging.getLogger("pi")


def run_pi_calculation(nb_million_points: int = DEFAULT_NB_MILLION_POINTS, nb_parallel_processes: int = 1) -> timedelta:
    logger.info("Run pi calculation with {} process(es)".format(nb_parallel_processes))

    start_time = time.monotonic()
    nb_points = nb_million_points * 1000000
    pi_value = pi_monte_carlo_parallel(nb_points, nb_parallel_processes)
    total_time = timedelta(seconds=time.monotonic() - start_time)

    logger.info(" -> The simple Monte-Carlo method with {}M random points gave pi = {} in {} seconds)".format(
        nb_million_points, pi_value, str(total_time.total_seconds())))
    return total_time


def run_pi_benchmark(nb_million_points: int = DEFAULT_NB_MILLION_POINTS,
                     range_processes: List[int] = range(1, (cpu_count() + 1) + 2), plot: bool = True) -> None:
    times = []
    cpu_load = []

    for proc in range_processes:
        cpu_time_a = (time.time(), psutil.cpu_times())
        delta_time = run_pi_calculation(nb_million_points=nb_million_points, nb_parallel_processes=proc)
        cpu_time_b = (time.time(), psutil.cpu_times())
        cpu_load.append(calculate(cpu_time_a[1], cpu_time_b[1]))
        times.append(delta_time.total_seconds())

    if plot is True:
        plx.plot(range_processes, times, xside="lower", yside="left", label="Time (seconds)")
        plx.plot(range_processes, cpu_load, xside="lower", yside="right", label="CPU load (%)")
        plx.xlabel("CPU count")
        plx.xticks(range_processes)
        plx.title('f(CPUs) = time and cpu_load')
        plx.show()
