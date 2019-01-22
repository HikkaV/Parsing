from scipy.special import expit
import Settings
import numpy as np
import os
import multiprocessing


class Helpers:

    def define_sitesqua_to_parse(self):
        """The func that regulates the available quantity of sites to parse"""
        if Settings.qua_sites - multiprocessing.cpu_count() > 0:
            return multiprocessing.cpu_count()
        else:
            return Settings.qua_sites

    def func(self, x):
        """
        A simple filter for some func
        deletes links which aren't valid
        """
        if x.__contains__("http") and x.__contains__("jpeg") or x.__contains__("http") and x.__contains__("jpg"):
            return 1

        else:
            return 0

    def make_dir(self, path):
        """

        path --path to dir where you want to save your dataset
        if dir doesn't exist , the func will make it

        """
        if not os.path.exists(path):
            os.mkdir(path)
            print("Dir was created " + path)

    def load_nn(self, filename='/home/hikkav/environments/my_env/models.npz'):
        """
            This function loads necessary parameters from npz file and returns them
            w -- weights
            b - biases

            """
        npz_members = np.load(filename)
        w = npz_members['weights']
        b = npz_members['biases']
        num_px = npz_members['num_px']
        return w, b, num_px
