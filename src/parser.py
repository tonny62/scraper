from bs4 import BeautifulSoup as bs

def parse(html):
    '''Parse html file, return dictionary of a company details.'''
    soup = bs(html)
    body = soup.body
    print(body)
    tbody = body.find_all('tbody')
    tbody = list(filter(smallest_tbody, tbody))
    tbody = list(filter(has_4td, tbody))   ## contains 1 company
    if(len(tbody) == 0):
        # Something weird happends
        return {}
    else:
        # Ex
        td = tbody[0].find_all('td')
        output = {}
        output['companynameTH'] = td[0].strong.text.strip()
        output['companynameEN'] = td[1].text.strip()
        output['companytype'] = td[2].text.split()[1]
        output['address'] = td[3].text.split(":")[1].strip()
        output['url'] = td[0].a.attrs.get('href')
        return output

def parse_a(html):
    soup = bs(html)
    body = soup.body
    table = body.find_all('table', recursive=False)[4]
    company_table = table.find_all('table')[3]
    datatd = company_table.find_all('td')[1].find_all('td')
    print(datatd[0])
    output = {}
    output['companynameTH'] = datatd[0].strong.text.strip()
    output['companynameEN'] = datatd[1].text.strip()
    output['companytype'] = datatd[2].text.split()[1]
    output['address'] = datatd[3].text.split(":")[1].strip()
    output['url'] = datatd[1].a.attrs.get('href') 
    return output

def parse(html):
    def table_filter(table):
        correct_attrs = {'width': '980', 'border': '0', 'cellspacing': '0', 'cellpadding': '0'}
        return correct_attrs == table.attrs

    soup = bs(html)
    tables = soup.find_all('table')
    correct_table = list(filter(table_filter, tables))[0]
    
    correct_table = bs(str(correct_table))

    tds = correct_table.find_all('td')[0].find_all('td')
    datatd = tds
    try:
        output = {}
        output['companynameTH'] = datatd[2].strong.text.strip()
        output['companynameEN'] = datatd[3].text.strip()
        output['companytype'] = datatd[4].text.split()[1]
        output['address'] = datatd[5].text.split(":")[1].strip()
        output['url'] = datatd[1].a.attrs.get('href') 
        return output
    except:
        return {"result":"error"}

    

def smallest_tbody(soup):
    return len(soup.find_all('tbody')) == 0

def has_4td(soup):
    return len(soup.find_all('td')) == 4
