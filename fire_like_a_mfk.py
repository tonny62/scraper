from bs4 import BeautifulSoup
from requests import Session
import warnings
warnings.filterwarnings('ignore')
import mysql.connector

def getDictFromFile(filename):
    with open("data/output3_nozerotype/"+filename, 'r', encoding='utf-8') as fin:
        ## create soup from the file
        text = BeautifulSoup(fin, "html5lib")
    try:
        ## create dictionary from fin (dbd scrape)
        mydict = dict(zip([item.string[:-2] for item in text.find_all("th")], [item.text.strip() for item in text.find_all("td")]))
        mydict.update({item.attrs['name'] : item.attrs['value'] for item in text.find_all('input')})            
    except:
        ## create empty row
        mydict = {"jpNo":file[:-5]}
    return mydict
   

def getDictFromSmelink(url, sess):
    def getCompanyDict(soup):
        def getClass(tbod):
            '''Find the tbody that itself is the company data container'''
            try:
                if("fontResult" in tbod.tr.td['class']):
                    return True
                else: return False
            except:
                return False
        def createCompanyDict(tbody):
            tds = tbody.find_all('td')
            com_dict = {}
            try:
                ## yet no better solution than hardcoding fields
                com_dict['nameTH'] = tds[0].text.strip()
                com_dict['nameEN'] = tds[1].text.strip()
                com_dict['type'] = tds[2].text.split(":")[1].strip()
                com_dict['location'] = tds[3].text.split(":")[1].strip()
                com_dict['link'] = tds[0].a['href']
            except:
                pass
            return com_dict
        company = list(filter(getClass, soup.body.find_all('tbody')))
        if(len(company) > 0):
            return createCompanyDict(company[0])
        else:
            return None
    print(os.getpid(),"sending request",url[-13:])
    page_html = sess.get(url, verify=False)
    print(os.getpid(),"done request",url[-13:])
    soup = BeautifulSoup(page_html.text, "html5lib")
    companydict = getCompanyDict(soup)
    return companydict

def generateTasks(count = 'All'):
    import os
#     from all file
#     if(count == 'All'):
#         tasks = os.listdir("data/output3_nozerotype")
#     else:
#         tasks = os.listdir("data/output3_nozerotype")[:count]
    import pickle
    with open("lefttasks.pickle", 'rb') as fin:
        tasks = pickle.load(fin)
    for task in tasks:
        url = "https://smelink.net/search?text={}".format(task.split(".")[0])
        yield url

def processLink(*args):
    url = args[0]
    sess = args[1]
    ## 1. getDictFromFile(filename)
    dict1 = getDictFromFile(url[-13:]+".html")
    ## 2. getDictFromSmelink(url)
    dict2 = getDictFromSmelink(url,sess)
    ## 3. compileDict
    dict1.update(dict2)
    compiledDict = dict1
    ## 4. insertIntoDb(Dict)
    insertIntoDb(compiledDict)
    ## 5. return compiledDict
    return compiledDict

def insertIntoDb(companyDict1):
    cnx = mysql.connector.connect(user='jobdatabaseroot', password='jobdatabaseroot', host='jobdatabase2.cieq9tyvhuue.ap-southeast-1.rds.amazonaws.com', database='company_db3', charset='utf8', use_unicode=True)
    try:
        cursor = cnx.cursor()
        data = (companyDict1.get('nameEN'), companyDict1.get('nameTH'), companyDict1.get('jpNo'), companyDict1.get('dataUpdatedDate'), 
        companyDict1.get('location'), companyDict1.get('type'), companyDict1.get('ที่ตั้ง'), companyDict1.get('ทุนจดทะเบียน (บาท)'), 
        companyDict1.get('ประเภทนิติบุคคล'), companyDict1.get('วัตถุประสงค์ (มาจากงบการเงินปีล่าสุด)'), companyDict1.get('สถานะนิติบุคคล'), 
        companyDict1.get('หมวดธุรกิจ (มาจากงบการเงินปีล่าสุด)'), companyDict1.get('โทรศัพท์'), companyDict1.get('E-mail address'))

        query = '''INSERT INTO `company` (`companynameEN`, `companynameTH`, `jpNo`, `dataUpdatedDate`, `location`,
            `type`, `address`, `capital`, `company_type`, `objective`, `status`, `category`, `telephone`, `email`) 
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');'''.format(*data)
        cursor.execute(query)
        cnx.commit()
    finally:
        cnx.close()
        
from requests import Session
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool
import os
import time
import math
import pickle

def threadWorker(intasks):
    print("me", os.getpid(), "starting with tasks size", len(intasks))
    sess = Session()
    sess.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0"}
    with ThreadPoolExecutor(max_workers=100) as executor:
        future = [executor.submit(processLink, task, sess) for task in intasks]
    return future

def chunker(data, chunksize):
    return [data[(i*chunksize) : (i+1)*(chunksize)] for i in range(int(math.ceil(len(data)/chunksize)))]

if(__name__=='__main__'):
    print("Entering")
    tasks = chunker(list(generateTasks()), 10)
    print("Numtasks", len(tasks))

    done = []
    st = time.time()
    
    try :
        with Pool(processes=10) as p:
            result = p.map_async(threadWorker, tasks)
            result.get()
    finally:
        en = time.time()
        print("End At", en-st)

    print("done", en-st)