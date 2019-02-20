import os
import os.path
from PIL import Image
import imghdr
import pygame
import neural_network
import numpy as np
import scipy
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt
import helper
from helper import Helpers


class Filters(object):

    def __init__(self, w, b, num_px):
        self.w = w
        self.b = b
        self.num_px = num_px
        self.helpers = Helpers()

    def define_car(self, x):
        """
         The function that filters files while using a simple implementation
         of Neural Network
         removes files that due to it's logic aren't cars
         """
        if os.path.exists(x):
            image = np.array(ndimage.imread(x, flatten=False))
            my_image = scipy.misc.imresize(image, size=(self.num_px, self.num_px)).reshape((1, self.num_px * self.num_px * 3)).T
            my_predicted_image = NeuralNetwork.predict(self.w, self.b, my_image)
            value = np.squeeze(my_predicted_image)
            print(value)
            if value == 1:
                print("Bad img was removed")
                os.remove(x)

    def compare_images(self, input_image, output_image):
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

    def find_duplicate_image(self, x):
        """
        The function searches for the same image in a folder , comparing pics dimensions , weight and quantity of pixels
        deletes founded duplicates
        :param x: the element of iterable collection
        """
        tmp = x
        tmp_list.remove(x)
        for z in tmp_list:
            if os.path.exists(tmp) and os.path.exists(z):
                if self.compare_images(Image.open(tmp), Image.open(z)):
                    print("The duplicate img was deleted")
                    os.remove(z)
            else:
                break

    def check_im_size(self, x):
        """
        Checks images due to their size
        invalid images are removed
        """
        img = pygame.image.load(x)
        width = img.get_width()
        height = img.get_height()
        if height < 80 or width < 80:
            if os.path.exists(x):
                print("IMG WITH INCORRECT SIZE WAS REMOVED")
                os.remove(x)

    def delete_bad_links(self, projects):
        """
        deletes links containing inappropriate words and so on
         """
        projects = (set(filter(self.helpers.func, projects)))
        projects = list(projects)
        return projects

    def check_file_on_trbl(self, x):
        """
        checks the image on troubles
        """
        global im
        try:
            im = Image.open(x)
            im.verify()
        except (OSError, FileNotFoundError):
            print("Error occurred")
            if os.path.exists(x):
                os.remove(x)
                print("Bad img was deleted")