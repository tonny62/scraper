from bs4 import BeautifulSoup as bs

def parse(html):
    '''Parse html file, return dictionary of a company details.'''
    soup = bs(html)
    body = soup.body
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

def smallest_tbody(soup):
    return len(soup.find_all('tbody')) == 0

def has_4td(soup):
    return len(soup.find_all('td')) == 4
