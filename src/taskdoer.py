import requests
from concurrent.futures import ThreadPoolExecutor
from src.parser import parse
from tqdm import tqdm
from src.sql import insert_into_db, get_task_done
import sys

def get_session():
    s = requests.Session()
    s.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) \
                 #Gecko/20100101 Firefox/60.0"}
    return s

def do_task_test():
    task = "0103554034290"
    session = get_session()
    request = send_get_request(task, session)
    return request

def send_get_request(task, session):
    '''Send a request to smelink, parse the request and insert into database'''    
    response = session.get("http://www.smelink.net/search?text={}".format(task), verify=False) # This line is blocking
    return response    

def do_task(task, session):
    '''Send a request to smelink, parse the request and insert into database'''    
    try:
        response = send_get_request(task=task, session=session)
        result = parse(response.text) # Do parsing
    except:
        pass
    finally:
        result['jpNo'] = task

    insert_into_db(result) # This line also is blocking
    return result

class mypbar():
    def __init__(self, lentask, order):
        self.pbar = tqdm(total=lentask, position=order)
        print("\n")

    def update(self):
        self.pbar.update()

def process_function(tasks, numthread, order):
    '''Do tasks using threads'''

    mysession = get_session()
    progressbar = mypbar(len(tasks), order)

    def callback(future):
        progressbar.update()

    with ThreadPoolExecutor(max_workers=numthread) as tpool:
        import os
#        print("Process {} has {} threads".format(os.getpid(), numthread))
        futures = [tpool.submit(lambda x:do_task(x, mysession),
            task) for task in tasks]  # do tasks
        [item.add_done_callback(callback) for item in futures] # add callback
        results = [future.result() for future in futures]
    return results

