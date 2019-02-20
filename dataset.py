
import numpy as np
import os
import h5py
import settings

def load_dataset():
    train_dataset = h5py.File(Settings.adress, "r")
    train_set_x_orig = np.array(train_dataset["train_img"][:])  # your train set features
    train_set_y_orig = np.array(train_dataset["train_labels"][:])  # your train set labels

    test_dataset = h5py.File(Settings.adress, "r")
    test_set_x_orig = np.array(test_dataset["test_img"][:])  # your test set features
    test_set_y_orig = np.array(test_dataset["test_labels"][:])  # your test set labels

    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig

