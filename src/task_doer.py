import requests

def get_session():
    s = requests.Session()
    s.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) \
                 Gecko/20100101 Firefox/60.0"}
    return s

def do_task(task, session):
    '''Send a request to smelink, parse the request and insert into database'''    
    response = session.get("https://smelink.net/search?text={}".format(task), verify=False) # This line s blocking
    
    ## There must be 2 parser: 1. DBD for industry 2. SME-Link for ENG Name
    result = parse(response.text) # Do parsing
    result['jpNo'] = task
    
    #insert(response) # This line also is blocking
    return result


