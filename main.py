from src import *
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import sys
import warnings
warnings.filterwarnings('ignore')    # suppress all warning
from tqdm import tqdm


def interactive_input():
    print("Number of Processes :", end="\t")
    np = int(input())
    print("Number of Threads   :", end="\t")
    nt = int(input())
    print("Target file         :", end="\t")
    tf = input()
    return np, nt, tf


if (__name__ == '__main__'):
    # Initialize arguments
    try:
        if(sys.argv[1] == '-i'):
            numProcesses, numThreads, taskFile = interactive_input()
            test = 0
        else:
            print("Using Test Configuration")
            raise
    except:
        numProcesses, numThreads, taskFile, test= 2, 20, None, 1
    
    print("numProcesses : {}, numThreads : {}, taskFile = {}, test = {}".format(
        numProcesses, numThreads, taskFile, test))

    # Create Tasks
    if(test):
        tasks = get_tasks_test()[:20]
    else:
        with open(taskFile, 'r') as fin:
            tasks = get_tasks(fin)
    
    tasks_chunks = chunk_splitter(tasks, numProcesses)

    tasks_chunks = [(tasks_chunks[i], numThreads, i) 
        for i in range(numProcesses)]

    # Do tasks with multiprocessing using multiple process
    with Pool(processes=numProcesses) as p:
        results_chunks = p.starmap(process_function, tasks_chunks, chunksize=1)

    import pickle
    with open("output.pickle", 'wb') as fout:
        pickle.dump(results_chunks, fout)
