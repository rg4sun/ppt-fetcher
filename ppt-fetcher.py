import os
import re
from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

site_url = 'http://www.chinacloud.cn'
base_url = 'http://www.chinacloud.cn/list.aspx?cid=13'



def get_html(baser_url:str, headers=headers)->str:
    try:
        response = requests.get(base_url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            print('Abnormal request, status_code={}'.format(response.status_code))
            return response.status_code
        return response.text
    except requests.exceptions.RequestException:
        print('Requests err, please check the inputed url')
        return None

def get_book_links(html_txt:str, site_url=site_url)->list:
    soup = BeautifulSoup(html_txt, 'html.parser')
    raw_link_list = soup.select('.nLink')
    link_list = [ site_url+'/'+ re.findall('href="(.*?)"', re.sub('&amp;', '&', str(raw_link)))[0] for raw_link in raw_link_list ]
    return link_list

def get_ppt_links(book_links:list, headers=headers)->list:
    for link in book_links:
        html_txt = get_html(link, headers=headers)
        