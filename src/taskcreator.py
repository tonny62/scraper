def get_tasks_test():
    '''Method for testing, use pickled data to test.'''
    with open("lefttasks.pickle", 'rb') as fin:
        tasks = pickle.load(fin)
    return tasks

def get_tasks(filein):
    '''Production function to retrieve data from csv file'''
    output = []
    for line in filein:
        output.append(line.split(",")[2])  # See the data
    return output
