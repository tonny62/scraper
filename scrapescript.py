def getCheckDigit(dig12):
    a= [int(dig12[item])*(13-item) for item in range(len(dig12))]
    b = sum(a)
    c = b%11
    return str(11-c)[-1]

def my_iterator():
    part1_comp = [str(item) for item in [0]]
    #part2_prov = [str(item) for item in [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,66,67,70,71,72,73,74,75,76,77,80,81,82,83,84,85,86,90,91,92,93,94,95,96]]
    part2_prov = [str(item) for item in [92,93,94,95,96]]
    part3_type = [str(item) for item in [2, 3, 4, 5, 6, 7, 8, 9]]
    ## 4xx -> 561
    part4_year = [item1 for item1 in [str(item) for item in range(561, 550,-1)]]
    part5_inde = [("0"*(5-len(item1))+item1) for item1 in [str(item) for item in range(1, 100000)]]
    #part6_chek = [str(item) for item in range(0,10)]

    for a in part1_comp:
        for b in part2_prov:
            for c in part3_type:
                for d in part4_year:
                    for e in part5_inde:
                        f = getCheckDigit(a+b+c+d+e)
                        yield a+b+c+d+e+f

                        
def get_index(dig13):
    return dig13[7:12]

def get_province(dig13):
    return dig13[1:3]


import os
import requests
import time
try:
    with requests.Session() as s:
        rawcookies = "JSESSIONID=5C4FA935A8069E94CCFA77C724DD0C9C; _ga=GA1.3.920439598.1528967744; BIGipServerDMZ_Server_Pool3=3087444160.20480.0000; _gid=GA1.3.1366849109.1530494613; _gat=1"
        cookies_jar = rawcookies.split(";")
        for item in cookies_jar:
            s.cookies[item.split("=")[0]] = item.split("=")[1]

        ## count how many jobs have been found
        foundcount = 0
        totalcount = 0
        notfound = 0     ## if found 5 consecutive 404 pages, start newtype
        next_type = 0    
        last_index = "0925556000966"

        starttime = time.time()
        lastprovtime = time.time()
        lastprov = "0"
        
        for item in my_iterator():
            if(get_province(item) !=lastprov):
                print("New Province", get_province(item))
                lastprov = get_province(item)
            if(next_type == 1):
                ## skip until start at next type
                if(get_index(item) == "99999"):
                    print("resume", item)
                    next_type = 0
                    notfound = 0
                pass
            elif(int(item) < int(last_index)):
                ## continue to the next job
                pass
            else:
                ## get job
                p = s.get("http://datawarehouse.dbd.go.th/bdw/est/details1.html?jpNo={}&jpTypeCode={}&t=".format(item, item[3]))
                if(p.status_code == 404):
                    ## not found job ; threshold 5 consecutive
                    notfound+=1
                    if(notfound == 10):
                        print("jump at", item)
                        next_type = 1
                        notfound = 0
                elif("กรุณาเข้าสู่ระบบใหม่" in p.text):
                    ## kicked from the system
                    last_index = item
                    totaltime = time.time() - starttime
                    print("Kicked : "+last_index+" "+str(totaltime))
                    break
                else:
                    ## found job
                    notfound = 0
                    filename = "output2_html/"+item+".html"
                    totalcount+=1
                    with open(filename, "w", encoding="utf-8") as fout:
                        fout.write(p.text)
                        foundcount+=1
                        if(foundcount%100==0):
                            print(filename,foundcount)
                    pass
                ## end if
        ## end for
except:
    print("item : ", item)
    print("Ended At : ", str(time.time() - starttime))
