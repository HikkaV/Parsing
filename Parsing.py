import time
from bs4 import BeautifulSoup
from selenium import webdriver
import httplib2
import os
import os.path
import re
import Settings
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from selenium.common import exceptions
import FIlterFunctions
from FIlterFunctions import Filters
import Helper


class Parser(object):

    def __init__(self, key, w, b, num_px, path, firstlen):
        self.path = path
        self.key = key
        self.w = w
        self.b = b
        self.num_px = num_px
        self.filters = Filters(self.w, self.b, self.num_px)
        self.firstlen = firstlen

    def gather_links(self, driver, SCROLL_PAUSE_TIME=2):
        global flag
        flag = False
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.select('img')
            projects = [table[i].get('src') for i in range(0, len(table))]
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            projects = self.filters.delete_bad_links(projects)
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(len(projects))
            if len(projects) >= self.key:
                return projects
            if last_height == new_height:
                flag = True
                return projects
            last_height = new_height

    def download(self, x):
        """This func downloads pics using their urls
         this is one of the most fastest methods for downloading files,
         as it uses caching
        """
        h = httplib2.Http('.cache')
        name = re.sub('/', '', x)
        response, content = h.request(x)
        abs_path = self.path + '/' + name + '.jpg'
        out = open(abs_path, 'wb')
        out.write(content)
        out.close()

    def parse(self, url, max_workers=50):
        driver = webdriver.Chrome(executable_path='/home/hikkav/environments/chromedriver')
        driver.get(url)

        while True:
            urls = self.gather_links(driver)

            with concurrent.futures.ThreadPoolExecutor(max_workers) as e:
                for i in urls:
                    e.submit(self.download, i)
                tmp_list = [self.path + '/' + x for x in os.listdir(self.path)]
                for z in tmp_list:
                    e.submit(self.filters.find_duplicate_image, z)
                path_list = [self.path + '/' + x for x in os.listdir(self.path)]
                for v in path_list:
                    e.submit(self.filters.check_file_on_trbl, v)
                tmp_list2 = [self.path + '/' + x for x in os.listdir(self.path)]
                for k in tmp_list2:
                    e.submit(self.filters.check_im_size, k)
            with concurrent.futures.ThreadPoolExecutor(max_workers) as ex:
                tmp = [self.path + '/' + m for m in os.listdir(self.path)]
                for o in tmp:
                    ex.submit(self.filters.define_car, o)
            if len(os.listdir(self.path)) - self.firstlen >= self.key or flag:
                driver.close()
                break
