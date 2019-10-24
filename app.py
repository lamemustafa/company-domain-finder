import requests
from bs4 import BeautifulSoup,SoupStrainer
from fuzzywuzzy import fuzz
import re
import cfscrape
import operator
import multiprocessing as mp
import argparse
import multiprocessing.pool
import os
from lxml import html

cfscrape.DEFAULT_CIPHERS = 'TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-'+\
    'AES256-SHA384'
scraper = cfscrape.create_scraper() 

HEADER ={
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'+\
    '*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) '+\
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 '+\
    'Safari/537.36',
}
POOL_COUNT = mp.cpu_count()
MIN_RATIO = 0.3333

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


def getDomainCrunchbase(link):
    temp5 = []
    c = scraper.get(link).content
    tree = html.fromstring(c)
    try:
        url = tree.xpath("//span[contains(text(), 'Website')]"+\
            "/../../../following::span[1]//a/@title")
        if url:
            l = url[0]
            if 'www.' in l:
                l = l.split('www.')[1]
            if '//' in l:
                l = l.split('//')[1]
            if '/' in l:
                l = l.split('/')[0]
            temp5.append(l.lower())	
    except Exception as e:
        pass
    return temp5

def getDomainTwitter(link):
    temp6 = []

    res = requests.get(link,headers=HEADER)
    if res.status_code == 200:
        c = res.content
        tree = html.fromstring(c)
        try:
            url = tree.xpath("//span[@class="+\
                "'ProfileHeaderCard-urlText u-dir']//a/@title")[0]
            l = url
            if 'www.' in l:
                l = l.split('www.')[1]
            if '//' in l:
                l = l.split('//')[1]
            if '/' in l:
                l = l.split('/')[0]
            temp6.append(l.lower())	
        except Exception as e:
            pass
    return temp6

def getDomainOwler(link):
    temp7 = []
    only_a_tags = SoupStrainer('div',{'class': 'website'})	
    c = scraper.get(link).content
    soup = BeautifulSoup(c,'html.parser',parse_only=only_a_tags)
    if soup.p:
        l = soup.p.a.get('href')
        if 'www.' in l:
            l = l.split('www.')[1]
        if '//' in l:
            l = l.split('//')[1]
        if '/' in l:
            l = l.split('/')[0]
        temp7.append(l.lower())	
    return temp7

def getDomainAngel(link):
    temp8 = []
    only_a_tags = SoupStrainer('li',{'class': 'websiteLink_daf63'})
    c = scraper.get(link).content
    soup = BeautifulSoup(c,'html.parser',parse_only=only_a_tags)
    if soup.a:
        l = soup.a.get('href')
        if 'www.' in l:
            l = l.split('www.')[1]
        if '//' in l:
            l = l.split('//')[1]
        if '/' in l:
            l = l.split('/')[0]
        temp8.append(l.lower())	
    return temp8

def getDomain(i,company_search):
    temp =[]
    temp8=[]
    temp5=[]
    temp6=[]
    temp7=[]
    only_div_tags = SoupStrainer('li',{'class': 'b_algo'})
    if i==1:
        res = requests.get('https://www.bing.com/search?q='+\
                    f'{company_search}',headers=HEADER)
        if res.status_code == 200:
            c = res.content
            soup = BeautifulSoup(c,'html.parser',
            parse_only=only_div_tags)
            for h2 in soup.findAll('h2'):
                if h2.a:
                    link = h2.a['href']
                    if '/wiki/' not in link and '//' in link:
                        link = link.split('//')[1].split('/')[0]
                        if 'www.' in link:
                            link = link.split('www.')[1]
                        if link not in temp:
                            temp.append(link.lower())
    
    if i==2:
        res = requests.get('https://www.bing.com/search?q=crunchbase:%20'+\
            f'{company_search}',headers=HEADER)
        temp1 = []
        if res.status_code == 200:
            c = res.content
            soup = BeautifulSoup(c,'html.parser',
                    parse_only=only_div_tags)
            for h2 in soup.findAll('h2'):
                if h2.a:
                    link = h2.a['href']
                    if 'www.crunchbase.com/organization/' in link and '//' in link:
                        temp1.append(link)
        pool1 = multiprocessing.Pool(5)
        temp5 = pool1.map(getDomainCrunchbase,[link for link in temp1])
    
    if i==3:
        res = requests.get('https://www.bing.com/search?q=twitter:%20'+\
            f'{company_search}',headers=HEADER)
        temp2 = []
        if res.status_code == 200:
            c = res.content
            soup = BeautifulSoup(c,'html.parser',
                    parse_only=only_div_tags)
            for h2 in soup.findAll('h2'):
                if h2.a:
                    link = h2.a['href']
                    if '//twitter.com/' in link and '/status/' not in link:
                        temp2.append(link)
        pool2 = multiprocessing.Pool(5)
        temp6 = pool2.map(getDomainTwitter,[link for link in temp2])

    if i == 5:
        res = requests.get('https://www.bing.com/search?q=owler:%20'+\
                    f'{company_search}',headers=HEADER)
        temp3 = []
        if res.status_code == 200:
            c = res.content
            soup = BeautifulSoup(c,'html.parser',
                    parse_only=only_div_tags)
            for h2 in soup.findAll('h2'):
                if h2.a:
                    link = h2.a['href']
                    if 'www.owler.com/company' in link:
                        temp3.append(link)
        pool3 = multiprocessing.Pool(POOL_COUNT)
        temp7 = pool3.map(getDomainOwler,[link for link in temp3])

    if i==4:
        res = requests.get('https://www.bing.com/search?q=angellist:%20'+\
            f'{company_search}',headers=HEADER)
        temp4 = []
        if res.status_code == 200:
            c = res.content
            soup = BeautifulSoup(c,'html.parser',
                    parse_only=only_div_tags)
            for h2 in soup.findAll('h2'):
                if h2.a:
                    link = h2.a['href']
                    if '//angel.co/' in link and '/jobs/' not in link:
                        if '/company/' in link or '/l/' in link:
                            temp4.append(link)
        pool4 = multiprocessing.Pool(5)
        temp8 = pool4.map(getDomainAngel,[link for link in temp4])

    dom_list = temp+temp5+temp6+temp7+temp8
    dom_list = [x for x in dom_list if x]
    return dom_list

def getResults(company_name):
    company_search = company_name.replace(' ','%20')
    pool0 = MyPool(5)
    data = pool0.starmap(getDomain, 
    [(i, company_name) for i in range(1,6)])
    pool0.close()
    pool0.join()
    doms= {}
    for i in data:
        for j in i:
            if isinstance(j,list):
                if j[0] in doms:
                    v = int(doms[j[0]])+1
                    doms.update({j[0]:v})
                else:
                    doms[j[0]]=1
            else:
                if j in doms:
                    v = int(doms[j])+1
                    doms.update({j:v})
                else:
                    doms[j]=1
    try:
        most_probable_domain = max(doms.items(), 
        key=operator.itemgetter(1))[0]
    except Exception as e:
        print('Please Try Again',e)
        exit()
    cnt=0
    max_score = 0
    other_option = None
    for i in doms.keys():
        score = fuzz.token_set_ratio(company_name,i)
        if int(score) >= 50:
            cnt+=int(doms[i])

    try:
        ratio = round(doms[most_probable_domain]/cnt,4)
        if ratio>1:
            ratio = MIN_RATIO
    except Exception as e:
        print('Please Try Again',e)
        exit()
    result = [company_name,most_probable_domain,cnt,ratio]
    print(doms)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
		description="Find domain name with the help of comapany name")
    parser.add_argument("company_name",help="Enter a company name",
	type=str)
    args = parser.parse_args()
    if args.company_name:
        company_name = args.company_name
        result = getResults(company_name)
        print(f'Company Name -> {result[0]} \t Domain -> {result[1]} '\
            +f'\t Similar Domains Count -> {result[2]} \t '+\
                f'Probability -> {result[3]}')
