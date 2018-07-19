import pickle

def get_tasks_test():
    '''Method for testing, use pickled data to test.'''
    with open("data/test.pickle", 'rb') as fin:
        tasks = pickle.load(fin)
    return tasks

def get_tasks(filein):
    '''Production function to retrieve data from csv file'''
    output = []
    for line in filein:
        output.append(line.strip())
    return output

