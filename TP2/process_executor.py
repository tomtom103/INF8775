import multiprocessing
import subprocess
import threading
from tqdm import tqdm

from functools import partial

from concurrent.futures import ProcessPoolExecutor, as_completed

def run_algorithm(lock: threading.Lock, run: list) -> None:
    algo, size, script = run
    output = subprocess.run(script, shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout

    formatted_output = ",".join(output.replace(" ", "").split("\n"))
    with lock:
        with open("result.csv", "a") as file:
            file.write(f"{algo},{size},{formatted_output}\n")

if __name__ == "__main__":
    runs = []

    with open("result.csv", "w") as file:
        file.write("algo,size,time,cost,final_path\n")


    for gl_size in [5, 10, 15, 20, 50, 100, 250, 500, 750, 1000, 1250]:
        for i in range(5):
            runs.append(["glouton", gl_size, f"python3 main.py -a glouton -e data/N{gl_size}_{i} -t -c"])
            runs.append(["approx", gl_size, f"python3 main.py -a approx -e data/N{gl_size}_{i} -t -c"])
    
    for dp_size in [5, 10, 15]:
        for i in range(3):
            runs.append(["progdyn", dp_size, f"python3 main.py -a progdyn -e data/DP_N{dp_size}_{i} -t -c"])

    runs.append(["progdyn", 20, f"python3 main.py -a progdyn -e data/DP_N20_0 -t -c"])

    retry = {}
    with tqdm(total=len(runs)) as pbar:
        with ProcessPoolExecutor(max_workers=5) as executor:
            lock = multiprocessing.Manager().Lock()

            data_to_future = {executor.submit(partial(run_algorithm, lock), run): run for run in runs}

            for future in as_completed(data_to_future):
                if future.exception():
                    data = data_to_future[future]
                    executor.submit(run_algorithm, lock, data)
                    retry[future] = data
                else:
                    useless = future.result()
                    pbar.update(1)

            for future in as_completed(retry):
                if future.exception():
                    data = retry[future]
                    print(f"Failed to run for: {data}")
                else:
                    useless = future.result()