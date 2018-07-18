if (__name__ == '__main__'):
    # create tasks
    with open("data/tasks.csv", 'r') as fin:
        tasks = createTasks(fin)
    # 
