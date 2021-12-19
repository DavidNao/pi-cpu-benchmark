from superpi.superpi import run_pi_calculation, run_pi_benchmark
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    run_pi_calculation(nb_parallel_processes=8)
    run_pi_benchmark()
