import time
from bs4 import BeautifulSoup
from selenium import webdriver
import httplib2
import os
import os.path
import re
import multiprocessing
from multiprocessing import Pool
from PIL import Image
import imghdr
import Settings
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from selenium.common import exceptions
import pygame
import cProfile
import pstats
import NeuralNetwork
import numpy as np
import h5py
import scipy
from PIL import Image
from scipy import ndimage
from NeuralNetwork import *
import matplotlib.pyplot as plt

def load_NN(filename='/home/hikkav/environments/my_env/models.npz'):
    npz_members = np.load(filename)
    w = npz_members['weights']
    b = npz_members['biases']
    num_px = npz_members['num_px']
    return w, b, num_px

def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print("Dir was created " + path)



def define_car(x):
        if os.path.exists(x):
           image = np.array(ndimage.imread(x, flatten=False))
           my_image = scipy.misc.imresize(image, size=(num_px, num_px)).reshape((1, num_px * num_px * 3)).T
           my_predicted_image = NeuralNetwork.predict(w, b, my_image)
           value = np.squeeze(my_predicted_image)
           if value==1:
             print("Bad img was removed")
             os.remove(x)



def parse(url, max_workers=50):
    global tmp
    driver = webdriver.Chrome(executable_path='/home/hikkav/environments/chromedriver')
    driver.get(url)

    while True:
        urls = gather_links(driver, key)

        with concurrent.futures.ThreadPoolExecutor(max_workers) as e:
            for i in urls:
                e.submit(download, i)
            tmp_list = [path + '/' + x for x in os.listdir(path)]
            for z in tmp_list:
                e.submit(find_duplicate_image, z)
            for v in path_list:
                e.submit(check_file_on_trbl, v)
            tmp = [path + '/'+ m for m in os.listdir(path)]
            for o in  tmp:
                e.submit(define_car, o)
            with concurrent.futures.ThreadPoolExecutor(max_workers) as ex:
                tmp_list2 = [path + '/' + x for x in os.listdir(path)]
                for k in tmp_list2:
                    ex.submit(check_im_size, k)
        if len(os.listdir(path)) - firstlen >= key or flag:
            driver.close()
            break


def func(x):
    if x.__contains__("http") and x.__contains__("jpeg") or x.__contains__("http") and x.__contains__("jpg"):
        return 1

    else:
        return 0


def gather_links(driver, key, SCROLL_PAUSE_TIME=2):
    global flag
    flag = False
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.select('img')
        projects = [table[i].get('src') for i in range(0, len(table))]
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        projects = delete_bad_links(projects)
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(len(projects))
        if len(projects) >= key:
            return projects
        if last_height == new_height:
            flag = True
            return projects
        last_height = new_height


def delete_bad_links(projects):
    projects = (set(filter(func, projects)))
    projects = list(projects)
    return projects


def check_file_on_trbl(x):
    global im
    try:
        im = Image.open(x)
        im.verify()
    except (OSError, FileNotFoundError):
        print("Error occurred")
        if os.path.exists(x):
            os.remove(x)
            print("Bad img was deleted")


def check_im_size(x):
    img = pygame.image.load(x)
    width = img.get_width()
    height = img.get_height()
    if height < 80 or width <80 :
        if os.path.exists(x):
            print("IMG WITH INCORRECT SIZE WAS REMOVED")
            os.remove(x)


def download(x):
    h = httplib2.Http('.cache')
    name = re.sub('/', '', x)
    response, content = h.request(x)
    abs_path = path + '/' + name + '.jpg'
    out = open(abs_path, 'wb')
    out.write(content)
    path_list.append(abs_path)
    out.close()


def define_sitesqua_to_parse():
    if Settings.qua_sites - multiprocessing.cpu_count() > 0:
        return multiprocessing.cpu_count()
    else:
        return Settings.qua_sites


def compare_images(input_image, output_image):
    # compare image dimensions (assumption 1)
    if input_image.size != output_image.size:
        return False

    rows, cols = input_image.size

    # compare image pixels (assumption 2 and 3)
    for row in range(rows):
        for col in range(cols):
            input_pixel = input_image.getpixel((row, col))
            output_pixel = output_image.getpixel((row, col))
            if input_pixel != output_pixel:
                return False

    return True


def find_duplicate_image(x):
    tmp = x
    tmp_list.remove(x)
    for z in tmp_list:
        if os.path.exists(tmp) and os.path.exists(z):
            if compare_images(Image.open(tmp), Image.open(z)):
                print("The duplicate img was deleted")
                os.remove(z)
        else:
            break


if __name__ == "__main__":
    w,b,num_px = load_NN()
    url = Settings.url
    path = Settings.path
    key = int(input())
    firstlen = len(os.listdir(path))
    path_list = list()
    make_dir(path)
    pool = Pool(processes=define_sitesqua_to_parse())
    pool.map(parse, url)
    print("The " + str(len(os.listdir(path)) - firstlen) + " pics were downloaded")
    cProfile.run('re.compile("foo|bar")', 'restats')
    p = pstats.Stats('restats')
    p.strip_dirs().sort_stats(-1).print_stats()
