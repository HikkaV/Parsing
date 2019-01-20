import multiprocessing
from multiprocessing import Pool
import Helper
from Helper import Helpers
import Parsing
from Parsing import Parser
import Settings
import os
if __name__ == "__main__":
    helpers = Helpers()
    w, b, num_px = helpers.load_nn()
    url = Settings.url
    path = Settings.path
    key = int(input())
    firstlen = len(os.listdir(path))
    parser = Parser(key, w, b, num_px, path, firstlen)
    helpers.make_dir(path)
    pool = Pool(processes=helpers.define_sitesqua_to_parse())
    pool.map(parser.parse, url)
    print("The " + str(len(os.listdir(path)) - firstlen) + " pics were downloaded")

