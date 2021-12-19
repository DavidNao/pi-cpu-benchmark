from random import uniform
import math
from multiprocessing import Pool
import logging
from typing import List

logger = logging.getLogger(__name__)


def get_chunk_list(nb_points: int, nb_parallel_processes: int) -> List[int]:
    if nb_parallel_processes == 1:
        return [nb_points]

    chunk_size = nb_points // (nb_parallel_processes * 128)
    if chunk_size == 0:
        return [nb_points]

    chunk_list = []
    quotient = nb_points // chunk_size
    if quotient > 0:
        chunk_list.extend(list(map(lambda x: chunk_size, range(0, quotient))))
    remainder = nb_points % chunk_size
    if remainder > 0:
        chunk_list.append(remainder)

    return chunk_list


def monte_carlo(nb_points: int) -> int:
    nbInside = 0
    # we pick a certain number of points (nbPoints)
    for i in range(nb_points):
        x = uniform(0, 1)
        y = uniform(0, 1)
        # (x, y) is now a random point in the square [0, 1] × [0, 1]
        if (x ** 2 + y ** 2) < 1:
            # This point (x, y) is inside the circle C(0, 1)
            nbInside += 1
    return nbInside


def make_log_result(results: List[int], chunk_list: List[int], print_log: bool):
    def log_result(retval):
        results.append(retval)
        if print_log is True:
            done = len(results) / len(chunk_list)
            logger.debug('{:.0%} done'.format(done))

    return log_result


def pi_monte_carlo_parallel(nb_points: int, nb_parallel_processes: int) -> float:
    """Returns a probabilist estimate of pi, as a float number."""
    pool = Pool(processes=nb_parallel_processes)
    chunk_list = get_chunk_list(nb_points, nb_parallel_processes)
    results = []
    print_log = 0
    print_frequency = 10 * nb_parallel_processes  # Print every 10 chunks * nb_parallel_processes
    for chunk in chunk_list:
        print_log += 1
        pool.apply_async(monte_carlo, args=[chunk],
                         callback=make_log_result(results, chunk_list, print_log % print_frequency == 0))
    pool.close()
    pool.join()
    nbInside = sum(results)
    return 4 * float(nbInside) / math.floor(nb_points)
