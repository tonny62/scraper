import requests
from concurrent.futures import ThreadPoolExecutor
from src.parser import parse
from tqdm import tqdm

def get_session():
    s = requests.Session()
    s.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) \
                 Gecko/20100101 Firefox/60.0"}
    return s

def do_task(task, session):
    '''Send a request to smelink, parse the request and insert into database'''    
    #print("Doing", task)
    try:
        response = session.get("https://www.smelink.net/search?text={}".format(task), verify=False) # This line s blocking
        ## There must be 2 parser: 1. DBD for industry 2. SME-Link for ENG Name
        result = parse(response.text) # Do parsing

    except:
        result = {"except":"error"}

    result['jpNo'] = task
    
    #insert(response) # This line also is blocking
    return result

class mypbar():
    def __init__(self, lentask, order):
        self.pbar = tqdm(total=lentask, position=order)

    def update(self):
        self.pbar.update()

def process_function(tasks, numthread, order):
    '''Do tasks using threads'''

    mysession = get_session()
    progressbar = mypbar(len(tasks), order)

    def callback(future):
        progressbar.update()
        #print(future.result()['jpNo'], "is Done") 


    with ThreadPoolExecutor(max_workers=numthread) as tpool:
        import os
        print("Process {} has {} threads".format(os.getpid(), numthread))
        futures = [tpool.submit(lambda x:do_task(x, mysession),
            task) for task in tasks]  # do tasks
        [item.add_done_callback(callback) for item in futures] # add callback
        results = [future.result() for future in futures]
    return results

