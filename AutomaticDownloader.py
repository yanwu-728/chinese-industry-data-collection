import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import shutil
import os
import pandas

url_99to02 = 'https://www.china-data-online.com/member/hynbefore2003/'
url_03to11 = 'https://www.china-data-online.com/member/hyn/'
url_12after = 'https://www.china-data-online.com/member/hyn2012/'

d = {
    url_99to02:[1999, 2003],
    url_03to11:[2003, 2012],
    url_12after: [1999, 2016]
}

def WebScrap(url):
    """
    Input:
    url: one of the links needed to be scaped.
    
    Output:
    industries: a dictionary where the key is the title of industry and value is the link for the
    'basic information'.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    industries = {}
    raw_industry_link = soup.findAll('a', class_="bluelink")
    for i in raw_industry_link:
        if i.attrs['href'][-4] in '0123456789':
            name = i.text[6:]
            browser = webdriver.Chrome(r'D:\Chinese Industrial Policy\chromedriver')
            new_url = url+'hyntshowjj.asp?hy='+i.attrs['href'][-4:]+'&code=A01'
            frontpage = 'https://www.china-data-online.com/'
            browser.get(frontpage)
            browser.get(new_url)
            for year in range(d[url][0], d[url][1]):
                select = Select(browser.find_element_by_id('ayear'))
                select.select_by_value(str(year))
                browser.find_element_by_link_text("[Save as]").click()
                time.sleep(1)
                shutil.move('C:\\Users\\dell\\Downloads\\mydata.xls', 'D:\\Chinese Industrial Policy\\Data Download\\'+str(year)+'\\'+name+'_'+str(year)+'.xls')

WebScrap(url_12after)


