
"""
Created on Sat Mar 28 18:30:51 2020

@author: axot
"""

import time
import argparse
from tqdm import tqdm
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
import requests



def parse_args(cmd=''):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-dp', '--driver_path', type=str, default='',
                        help='path to your chrome driver')
    
    parser.add_argument('-t', '--sleep_time', type=float, default=0,
                        help='sleep_time after your driver get info')
    
    parser.add_argument('-k', '--keyword', type=str,
                        help='search keyword')
    
    parser.add_argument('-p', '--pages', type=int, nargs='*', default=[0, 0],
                        help='your start page and end page')
    
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
        self.number_filter = '0123456789.'
        
        
        # check if we want to use webdriver to get html after js render
        if driver_path != '':
            self.driver = webdriver.Chrome(driver_path)
        else:
            self.driver = None
        self.sleep_time = sleep_time
        
         
    def __del__(self):
        if self.driver is not None:
            self.driver.close()
            
    def get_float_number(self, text):
        return float(''.join(filter(lambda ch: ch in self.number_filter, text)))
        
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
        
        # get average price
        prices = product_info.find("div", class_="_3n5NQx").contents[0].split('-')
        prices = [self.get_float_number(p) for p in prices]
        avg_price = sum(prices) / len(prices)
        
        
        rating = float(product_info.find("div", class_="_3Oj5_n _2z6cUg").contents[0])
        
        comments_num = float(product_info.find_all("div", class_="_3Oj5_n")[1].contents[0])
        
        sold_num = float(product_info.find("div", class_="_22sp0A").contents[0])
        
        style_num = len(product_info.find_all("div", class_="flex items-center crl7WW")[0].find_all("button"))
        
        img_num = len(soup.find_all("div", class_="_2MDwq_"))
        
        description_len = len(soup.find("div", class_="_2u0jt9").find('span').contents[0])
        
        remain_num = self.get_float_number(product_info.find("div", class_="_1FzU2Y").find_all('div')[-1].contents[0])
        
        
        try:
            transport_free = self.get_float_number(product_info.find("div", class_="_2mwtMq").contents[0])
        except:
            transport_free = None
        
        try:
            seller_name = soup.find("div", class_="_3Lybjn").contents[0]
        except:
            seller_name = None
        
        
        return [avg_price, rating, comments_num, sold_num, style_num,
                img_num, description_len, remain_num, transport_free, seller_name]
        
    def get_all_product_csv(self, save_name, products_name_page):
        '''
        get product info csv (without seller info)

        Parameters
        ----------
        save_name : str
            output csv save name
            
        products_name_page : int
            .products page in search result

        Returns
        -------
        None

        '''
        
        columns = ['product_name', 'page', 'avg_price', 'rating', 'comments_num', 'sold_num', 'style_num',
                   'img_num', 'description_len', 'remain_num', 'transport_free', 'seller_name']
        
        products_info_list = []
        for product_name_page in tqdm(products_name_page):
            try:
                products_info_list.append([product_name_page[0]] +  [product_name_page[1]] + self.get_product_info(product_name_page[0]))
            except KeyboardInterrupt:
                return -1
            except:
                pass
        
        product_infos = pd.DataFrame(columns=columns, data=products_info_list)
        product_infos.to_csv(save_name, index=None)
        
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
        
        if seller_name is None:
            return [None] * 7
        
        # get html
        url = self.base_url + str(seller_name)
        pageSource = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(pageSource, 'lxml')
        
        # get seller info
        seller_page = soup.find('div', class_='section-seller-overview-horizontal__seller-info-list')
        if seller_page is None:
            return [None] * 7
        seller_info = [item.contents[0] 
                       for item in seller_page.find_all("div", class_="section-seller-overview__item-text-value")]
        
        # sometimes there is no canceled rate in seller info
        if len(seller_info) >= 13:
            product_num = seller_info[0]
            watching = seller_info[2]
            response_rating = self.get_float_number(seller_info[4]) * 0.01
            canceled_rate = self.get_float_number(seller_info[6]) * 0.01
            follower_num = seller_info[8]
            comment_info = seller_info[10].split(' ')
            comment_rating = float(comment_info[0])
            comment_num = comment_info[1]
        else:
            product_num = seller_info[0]
            watching = seller_info[2]
            response_rating = self.get_float_number(seller_info[4]) * 0.01
            canceled_rate = None
            follower_num = seller_info[6]
            comment_info = seller_info[8].split(' ')
            comment_rating = comment_info[0]
            comment_num = comment_info[1]
        
        return [product_num, watching, response_rating, canceled_rate, follower_num,
                comment_rating, comment_num]
      
        
    def get_seller_infos(self, seller_name_list):
        '''
        get all seller infos by seller name list

        Parameters
        ----------
        seller_name_list : str[]
            seller name list

        Returns
        -------
        seller_infos : auto[]
            all seller info

        '''
        
        seller_infos = {}
        for seller_name in seller_name_list:
            if not seller_infos.__contains__(seller_name):
                seller_infos[seller_name] = self.get_seller_info(seller_name)
        
        return seller_infos
        
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
        
        products_name_page = []
        for page in range(start_page, end_page + 1):
            print('searching page:', page)
            url = self.base_url + 'search?keyword=%s&page=%d' % (keyword, page)
            
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')
        
            all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
            for item in all_items:
                products_name_page.append((item.find('a').get('href'), page))
            
        return products_name_page
        
    
    def get_allcsv(self, keyword, start_page, end_page):
        '''
        Description
            get product info csv by search keyword from start_page to end_page

        Parameters
        ----------
        keyword : str
            search keyword.
            
        start_page : int
            start search page
            
        end_page : TYPE
            end search page

        Returns
        -------
        None.

        '''
        
        products_name_page = self.get_search_page_products_name(keyword, start_page, end_page)
        
        # get product info
        print('get product info')
        save_name = keyword + '_product_infos_page%d-%d.csv' % (start_page, end_page)
        self.get_all_product_csv(save_name, products_name_page)
        csv = pd.read_csv(save_name)
        
        # get seller_info
        print('get seller_info')
        seller_info_column = ['product_num', 'watching', 'response_rating', 'canceled_rate', 
                              'follower_num','comment_rating', 'comment_num']
        sellers_name_list = csv['seller_name']
        seller_infos = self.get_seller_infos(sellers_name_list)
        
        
        # match seller_info by product_info[seller_name]
        print('matching')
        seller_data = []
        for seller_name in sellers_name_list:
            seller_data.append(seller_infos[seller_name])
        
        # combine csv
        seller_csv = pd.DataFrame(data=seller_data, columns=seller_info_column)
        csv = pd.concat([csv, seller_csv], axis=1)
        csv.to_csv(save_name, index=None)
        
        
        

if __name__ == "__main__":
    args = parse_args()
    
    shopee_crapper = ShopeeCrawler(driver_path=args.driver_path, sleep_time=args.sleep_time)
    shopee_crapper.get_allcsv(args.keyword, start_page=args.pages[0], end_page=args.pages[1])
    
    
    del shopee_crapper






        
        
