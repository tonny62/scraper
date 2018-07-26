import pickle
from src.sql import get_task_done

def get_tasks_test():
    '''Method for testing, use pickled data to test.'''
    with open("data/test.pickle", 'rb') as fin:
        tasks = pickle.load(fin)[:20]
    
    output = list(set(tasks).difference(get_task_done()))
    return output

def get_tasks(filein):
    '''Production function to retrieve data from csv file'''
    output = []
    
    for line in filein:
        output.append(line.strip())
    
    output = list(set(output).difference(get_task_done()))
    return output


