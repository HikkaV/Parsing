import multiprocessing
from multiprocessing import Pool
import helper
from helper import Helpers
import parsing
from parsing import Parser
import settings
import os
if __name__ == "__main__":
    helpers = Helpers()
    w, b, num_px = helpers.load_nn()
    url = settings.url
    path = settings.path
    key = int(input())
    helpers.make_dir(path)
    firstlen = len(os.listdir(path))
    parser = Parser(key, w, b, num_px, path, firstlen)
    pool = Pool(processes=helpers.define_sitesqua_to_parse())
    pool.map(parser.parse, url)
    print("The " + str(len(os.listdir(path)) - firstlen) + " pics were downloaded")
