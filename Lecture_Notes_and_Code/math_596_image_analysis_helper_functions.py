import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io

# We need a tool that converts images into grayscale (i.e. all pixel values in [0, 1])
def gray_scale_convert(image):
    rescaled_image = np.zeros((image.shape[0], image.shape[1]))
    rescaled_image[:, :] = image
    rescaled_image -= np.min(rescaled_image)
    rescaled_image /= np.max(rescaled_image)
    return rescaled_image

# We need to be able to pass in a directory and build an image list
def file_builder(directory):
    image_list = []
    # iterate over files in
    # that directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename != "Readme":
                input_image = gray_scale_convert(np.squeeze(io.imread(os.path.join(root, filename))) )
                image_list.append( input_image )
    return image_list

# We would like to easily comapre different images to one another after we do various things to them.  
def image_comparison(original_image, reduced_image):
    gscale_reduced_image = gray_scale_convert(reduced_image) # note, we need to make sure skinny_puppy is grayscale
    difference = np.abs( original_image - gscale_reduced_image )

    fig, axes = plt.subplots(1, 3, figsize=(10, 5))
    ax = axes.ravel()
    ax[0].imshow(original_image, cmap=plt.cm.gray)
    ax[0].set_title("Original")
    ax[1].imshow(gscale_reduced_image, cmap=plt.cm.gray) 
    ax[1].set_title("Reduced")
    ax[2].imshow(difference, cmap=plt.cm.gray)
    ax[2].set_title("Difference")
    fig.tight_layout()

def zero_mean(mat):
    avg_mat = np.tile(np.mean(mat, axis=1).reshape(-1, 1), (1, mat.shape[1]))
    zero_avg_mat = mat - avg_mat
    return zero_avg_mat, avg_mat

def mode_builder(data_mat):
    zero_avg_data, _ = zero_mean(data_mat)
    u, s, vh = np.linalg.svd(zero_avg_data, full_matrices=False)
    return u, s

def mode_selector(u, s, thrshhld):
    indskp = np.log10(s/s[0]) >= -thrshhld
    return u[:, indskp]

def mode_projector(data_mat, u):
    return u @ (u.T @ data_mat)