from src import *
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import sys
import warnings
warnings.filterwarnings('ignore')    # suppress all warning
from tqdm import tqdm
import time

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
        elif(sys.argv[1] == '-d'):
            numProcesses, numThreads, taskFile = 2, 25, 'data/firmID_DBD.csv'
            test = 0
        else:
            print("Using Test Configuration")
            raise
    except:
        numProcesses, numThreads, taskFile, test= 2, 5, None, 1

    print("\n"*3)   
    print("numProcesses : {}, numThreads : {}, taskFile = {}, test = {}".format(
        numProcesses, numThreads, taskFile, test))
    print("\n"*3)

    # Create Tasks
    if(test):
        tasks = get_tasks_test()
    else:
        with open(taskFile, 'r') as fin:
            tasks = get_tasks(fin)
 
#    limit = 5000
#    if(len(tasks) < limit):
#        pass
#    else:
#        newtask = []
#        for i in range(limit):
#            newtask.append(tasks[i])
#        print("Limit at", limit)
#
    tasks_chunks = chunk_splitter(tasks, numProcesses)
    tasks_chunks = [(tasks_chunks[i], numThreads, i) for i in range(numProcesses)]
    
    time.sleep(2)
    # Do tasks with multiprocessing using multiple process
    with Pool(processes=numProcesses) as p:
        results_chunks = p.starmap(process_function, tasks_chunks)
        print("hi")
