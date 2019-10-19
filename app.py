import requests
import argparse
from fuzzywuzzy import fuzz
import os
import time
import pandas as pd
from googlesearch import search
import multiprocessing as mp

def getResults(line):

    company_name = line.strip().replace('\n','')
    company = company_name.lower().replace(' ','%20')
    flag = False
    domain = None
    max_score = 0
    req = requests.get('https://autocomplete.clearbit.com/'\
    +f'v1/companies/suggest?query={company}')
    
    if req.status_code == 200:

        
        data = req.json()

        for i in data:

            dom = str(i['domain']).split('.')[0]
            score = fuzz.token_set_ratio(company_name,dom)

            if score > max_score:

                max_score=score
                domain=i['domain'].replace('\n','')

        if domain:

            flag = True
    
        else:

            flag=False
    
    if not flag:

        response = search(company_name, stop=10,pause=1)
        temp=[]

        for r in response:

            if 'www.' in r:

                r = r.split('www.')[1].split('/')[0]
                
            else:
                r = r.split('//')[1].split('/')[0]

            if r not in temp:
                temp.append(r)
                score = fuzz.token_set_ratio(company_name,
                r.split('.')[0])

                if score > max_score:

                    max_score=score
                    domain=r.replace('\n','')

    data = [company_name,domain,max_score]              
    return data

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Find domain name with the help of comapany name")
    parser.add_argument("company_name",help="Enter a company name",
    type=str)
    parser.add_argument('-f','--filepath',help='Enter a file path',
    action="store_true")
    args = parser.parse_args()
    

    if not args.filepath:

        company_name = args.company_name
        data = getResults(company_name)
        print(f'Company Name -> {data[0]} \t Domain -> {data[1]} '\
            +f'\t Prediction Confidence Score {data[2]}')

    else:

        file_path = os.path.abspath(args.company_name)
        dom_data = []
        pool = mp.Pool(mp.cpu_count())

        with open(file_path) as source_file:

            results = pool.map(getResults, source_file, 1)

        pool.close()
        pool.join()

        df_domains = pd.DataFrame(data=results)
        df_domains.columns = ['Company Name','Domain',
        'Prediction Confidence Score']
        df_domains.to_csv(str(f'results_{int(time.time())}'),sep='\t')
        df_domains.to_json(str(f'results_{int(time.time())}_json'),
        orient='records')
