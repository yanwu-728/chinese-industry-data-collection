import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import csv
import glob
import xlrd

url_99to02 = 'https://www.china-data-online.com/member/hynbefore2003/'
url_03to11 = 'https://www.china-data-online.com/member/hyn/'
url_12after = 'https://www.china-data-online.com/member/hyn2012/'
urls = [url_99to02, url_03to11, url_12after]

d = {
    url_99to02:[1999, 2003],
    url_03to11:[2003, 2012],
    url_12after: [1999, 2016]
}

def GetIndustryCode(urls):
    industry_code = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    for index in range(3):
        response = requests.get(urls[index], headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        industries = {}
        raw_industry_link = soup.findAll('a', class_="bluelink")
        for i in raw_industry_link:
            if i.attrs['href'][-4] in '0123456789':
                name = i.text[6:]
                industry_code[name] = i.attrs['href'][-4:]
    return industry_code

industry_code = GetIndustryCode(urls)
headers = [
        'Year', 
        'Industry', 
        'Industry Code', 
        'District',
        'Number of Enterprises(unit)',
        'Number of Loss-marking Enterprises(unit)',
        'Gross Industrial Output Value(at current price)(1,000 yuan)',
        'Industrial sales value of output(current price)(1,000 yuan)',
        'Industrial sales value of output(current price)_export turnover(1,000 yuan)',
        'Number of Employees(person)',
        'Industrial Value-added(1,000 yuan)',
        'Accrued payroll(1,000 yuan)',
        'Taxes payable(1,000 yuan)'
        ]

def Merger():
    count = 0
    with open('MasterView.csv', 'w', encoding='UTF8') as MasterView:
        writer = csv.writer(MasterView)
        writer.writerow(headers)
        for i in range(1999, 2016):
            direc = 'D:\Chinese Industrial Policy\ChineseDataOnlineYearlyData\\'+str(i)
            path = os.getcwd()
            files = os.listdir(direc)
            for f in glob.glob(direc+'\*.xls'):
                df = pd.read_html(f)
                f = f[62:]
                data = [i, f[:-9], industry_code[f[:-9]]]
                for index, row in df[2].iterrows():
                    r = row.values.tolist()
                    if row.isnull().values.all():
                        continue
                    else:
                        if len(r) == 10:
                            newdata = data + r
                        else:
                            newdata = data + [r[0], r[1], r[2], r[3], 'nan', 'nan', r[5], r[4], r[6], 'nan']
                        writer.writerow(newdata)
                count += 1
                if count%200 == 0:
                    print(count/14000)

Merger()