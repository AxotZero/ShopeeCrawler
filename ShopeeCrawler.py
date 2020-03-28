
"""
Created on Sat Mar 28 18:30:51 2020

@author: asdsw
"""

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import argparse


def parse_args(cmd=''):
    
    parser = argparse.ArgumentParser()
    # parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-dp', '--driver_path', type=str, default='',
                        help='your driver path')
    parser.add_argument('-t', '--sleep_time', type=float, default=0,
                        help='driver path')
    
    if cmd != '':
        return parser.parse_args(cmd)
    else:
        return parser.parse_args()
    
    
class ShopeeCrawler():
    
    def __init__(self, driver_path='', sleep_time=0):
        
        self.base_url = f'https://shopee.tw/'
        
        self.headers = {
            'User-Agent': 'Googlebot',
            'From': 'YOUR EMAIL ADDRESS'
        }
        
        # check if we want to use webdriver to get html after js render
        if driver_path != '':
            self.driver = webdriver.Chrome(driver_path)
        else:
            self.driver = None
        self.sleep_time = sleep_time
        
    def __del__(self):
        if self.driver is not None:
            self.driver.close()
        
    def get_product_info(self, product_name):
        '''
        Description:
            get seller info by product_name

        Parameters
        ----------
        product_name : str
            product name.

        Returns
        -------
        product_info : dict

        '''
        
        url = self.base_url + product_name
        
        if self.driver is not None:
            self.driver.get(url)  
            time.sleep(self.sleep_time)
            pageSource = self.driver.page_source  
        else:
            pageSource = requests.get(url, headers=self.headers).text
        
        soup = BeautifulSoup(pageSource, 'lxml')
        
        product_info = soup.find("div", class_="flex flex-auto k-mj2F")
        
        prices = product_info.find_all("div", class_="_3n5NQx")
        
        rating = product_info.find("div", class_="_3Oj5_n _2z6cUg")
        
        comments_num = product_info.find_all("div", class_="_3Oj5_n")
        
        sold_num = product_info.find_all("div", class_="_22sp0A") 
        
        style_num = len(product_info.find_all("div", class_="flex items-center crl7WW")[0].find_all("button"))
        
        img_num = len(soup.find_all("div", class_="_2MDwq_"))
        
        description_len = len(soup.find("div", class_="_2u0jt9").find('span').contents[0])
        
        transport_free = product_info.find_all("div", class_="_2mwtMq")
        
        seller_name = soup.find("div", class_="_3Lybjn")
        
        print('=' * 50)
        print('product info:')
        print('product_name:', product_name)
        print('pricies:\t', [p.contents[0] for p in prices])
        print('rating:\t', rating.contents[0])
        print('comments_num:\t', comments_num[1].contents[0])
        print('sold_num:\t', sold_num[0].contents[0])
        print('style_num:\t', style_num)
        print('img_num:\t', img_num)
        print('description_len:', description_len)
        
        try: 
            print('transport_free:', transport_free[0].contents)
        except:
            print('transport_free:\t None')
        
        try:
            print('seller_name:\t', seller_name.contents)
        except:
            print('seller_name:\t None')
        
    def get_seller_info(self, seller_name):
        '''
        Description:
            get seller info by name

        Parameters
        ----------
        seller_name : str
            seller name.

        Returns
        -------
        seller_info : dict

        '''
        
        url = self.base_url + seller_name
        pageSource = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(pageSource, 'lxml')
        
        seller_page = soup.find('div', class_='section-seller-overview-horizontal__seller-info-list')
        seller_info = [item.contents[0] 
                       for item in seller_page.find_all("div", class_="section-seller-overview__item-text-value")]
        
        product_num = seller_info[0]
        watching = seller_info[2]
        response_rating = seller_info[4]
        canceled_rate = seller_info[6]
        follower_num = seller_info[8]
        comment_info = seller_info[10]
        attend_time = seller_info[-1]
        
        print('=' * 50)
        print('seller info:')
        print('seller name:\t', seller_name)
        print('product_num:\t', product_num)
        print('watching:\t', watching)
        print('response_rating:', response_rating)
        print('canceled_rate:\t', canceled_rate)
        print('follower_num:\t', follower_num)
        print('comment_info:\t', comment_info)
        print('attend_time:\t', attend_time)
                
    def get_search_page_products_name(self, keyword, start_page=0, end_page=0):
        '''
        Description:
            Get products name list by search keyword
        
        Parameters
        ----------
        keyword : str
            shopee search keyword.
            
        start_page : TYPE, optional
            start page to search. default is 0    
        
        end_page : TYPE, optional
            end page to search. The default is 0.

        Returns
        -------
        products_name : str[]
            products name list

        '''
        
        products_name = []
        for page in range(start_page, end_page + 1):
        
            url = self.base_url + 'search?keyword={keyword}&page={page}&sortBy=relevancy'
            
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')
        
            all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
            for item in all_items:
                products_name.append(item.find('a').get('href'))
        
        return products_name
        

if __name__ == "__main__":
    args = parse_args()
    
    # shopee_crapper = ShopeeCrapper(driver_path=args.driver_path, sleep_time=args.sleep_time)
    
    # debug
    shopee_crapper = ShopeeCrawler(driver_path='', sleep_time=0)
    shopee_crapper.get_product_info('/🔥任選5件680🔥高品質潮T-純棉圓領短袖T恤-FILA-印花T恤-男裝-大尺碼短T-大尺寸男T-現貨出售-i.199006536.7417997413')
    shopee_crapper.get_seller_info('dssss455eeds5')
    
    del shopee_crapper






        
        
