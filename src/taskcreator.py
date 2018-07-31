import pickle
from src.sql import get_task_done
import time

def read_testdata():
    '''Method for testing, use pickled data to test.'''
    with open("data/test.pickle", 'rb') as fin:
        tasks = pickle.load(fin)
    return tasks

def get_tasks_test(length=2000):
    data = read_testdata()
    output = list(set(data).difference(get_task_done()))
    if(len(output) < length):
        pass
    else:
        output = output[:length]
    print("Task Created : ", len(output))
    return output


def get_tasks(filein):
    '''Production function to retrieve data from csv file'''
    output = []
    for line in filein:
        output.append(line.strip())
    
    output = list(set(output).difference(get_task_done()))[:500]
    print("Task Created : ", len(output))
    return output


